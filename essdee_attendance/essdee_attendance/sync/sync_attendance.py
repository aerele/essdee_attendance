import requests
import datetime
import json
import os
import sys
import time
import logging
from logging.handlers import RotatingFileHandler
import pickledb
from zk import ZK
import frappe
from erpnext.hr.doctype.employee_checkin.employee_checkin import add_log_based_on_employee_field

device_punch_values_IN = [0,4]
device_punch_values_OUT = [1,5]
logs_directory = 'logs'

def sync_device(ip, port=4370, timeout=30):
	zk = ZK(ip, port=port, timeout=timeout)
	conn = zk.connect()
	return conn

def setup_logger(name, log_file, level=logging.INFO, formatter=None):
	if not formatter:
		formatter = logging.Formatter('%(asctime)s\t%(levelname)s\t%(message)s')

	handler = RotatingFileHandler(log_file, maxBytes=10000000, backupCount=50)
	handler.setFormatter(formatter)

	logger = logging.getLogger(name)
	logger.setLevel(level)
	if not logger.hasHandlers():
		logger.addHandler(handler)

	return logger

# setup logger and status
if not os.path.exists(logs_directory):
    os.makedirs(logs_directory)
error_logger = setup_logger('error_logger', '/'.join([logs_directory, 'error.log']), logging.ERROR)
info_logger = setup_logger('info_logger', '/'.join([logs_directory, 'logs.log']))
status = pickledb.load('/'.join([logs_directory, 'status.json']), True)


def sync_attendance_log():
	settings = frappe.get_single('Essdee Attendance Settings')
	if settings.sync_attendance_logs:
		try:
			last_lift_off_timestamp = _safe_convert_date(status.get('lift_off_timestamp'), "%Y-%m-%d %H:%M:%S.%f")
			if (last_lift_off_timestamp and last_lift_off_timestamp < datetime.datetime.now() - datetime.timedelta(minutes=settings.pull_frequency)) or not last_lift_off_timestamp:
				status.set('lift_off_timestamp', str(datetime.datetime.now()))
				info_logger.info("Cleared for lift off!")
				for device in settings.device_details:
					device_doc = frappe.get_doc('Essdee Biometric Device', device.device_id)
					device_attendance_logs = None
					info_logger.info("Processing Device: "+ device_doc.device_id)
					dump_file = logs_directory+'/'+device_doc.ip.replace('.', '_')+'_last_fetch_dump.json'
					if os.path.exists(dump_file):
						info_logger.error('Device Attendance Dump Found in Log Directory. This can mean the program crashed unexpectedly. Retrying with dumped data.')
						with open(dump_file, 'r') as f:
							file_contents = f.read()
							if file_contents:
								device_attendance_logs = list(map(lambda x: _apply_function_to_key(x, 'timestamp', datetime.datetime.fromtimestamp), json.loads(file_contents)))
					try:
						pull_process_and_push_data(settings, device_doc, device_attendance_logs)
						status.set(f'{device_doc.device_id}_push_timestamp', str(datetime.datetime.now()))
						if os.path.exists(dump_file):
							os.remove(dump_file)
						info_logger.info("Successfully processed Device: "+ device_doc.device_id)
					except:
						error_logger.exception('exception when calling pull_process_and_push_data function for device'+json.dumps(device_doc, default=str))
				shift_type_device_map_list = shift_type_device_map(settings.device_details)
				if shift_type_device_map_list:
					update_shift_last_sync_timestamp(shift_type_device_map_list)
				status.set('mission_accomplished_timestamp', str(datetime.datetime.now()))
				info_logger.info("Mission Accomplished!")
		except:
			error_logger.exception('exception has occurred in the sync attendance log function...')
	else:
		frappe.log_error(
			_("Hourly sync of attendance logs is not enabled in essdee attendance settings")
		)

def pull_process_and_push_data(settings, device, device_attendance_logs=None):
	attendance_success_log_file = '_'.join(["attendance_success_log", device.device_id])
	attendance_failed_log_file = '_'.join(["attendance_failed_log", device.device_id])
	attendance_success_logger = setup_logger(attendance_success_log_file, '/'.join([logs_directory, attendance_success_log_file])+'.log')
	attendance_failed_logger = setup_logger(attendance_failed_log_file, '/'.join([logs_directory, attendance_failed_log_file])+'.log')
	if not device_attendance_logs:
		device_attendance_logs = fetch_attendance(device)
		if not device_attendance_logs:
			return
	index_of_last = -1
	last_line = get_last_line_from_file('/'.join([logs_directory, attendance_success_log_file])+'.log')
	import_start_date = _safe_convert_date(settings.import_start_date, "%Y%m%d")
	if last_line or import_start_date:
		last_user_id = None
		last_timestamp = None
		if last_line:
			last_user_id, last_timestamp = last_line.split("\t")[4:6]
			last_timestamp = datetime.datetime.fromtimestamp(float(last_timestamp))
		if import_start_date:
			if last_timestamp:
				if last_timestamp < import_start_date:
					last_timestamp = import_start_date
					last_user_id = None
			else:
				last_timestamp = import_start_date
		for i, x in enumerate(device_attendance_logs):
			if last_user_id and last_timestamp:
				if last_user_id == str(x['user_id']) and last_timestamp == x['timestamp']:
					index_of_last = i
					break
			elif last_timestamp:
				if x['timestamp'] >= last_timestamp:
					index_of_last = i
					break

	for device_attendance_log in device_attendance_logs[index_of_last+1:]:
		punch_direction = device.punch_direction
		if punch_direction == 'AUTO':
			if device_attendance_log['punch'] in device_punch_values_OUT:
				punch_direction = 'OUT'
			elif device_attendance_log['punch'] in device_punch_values_IN:
				punch_direction = 'IN'
			else:
				punch_direction = None

		employee = frappe.db.get_value('Employee',{'attendance_device_id': device_attendance_log['user_id']})
		checkin_record = frappe.db.get_value('Employee Checkin',
						{
							'employee':employee,
							'time':device_attendance_log['timestamp'],
							'device_id': device.device_id,
							'log_type': punch_direction
						})
		if not checkin_record:
			add_log_based_on_employee_field(device_attendance_log['user_id'], device_attendance_log['timestamp'], device.device_id, punch_direction)


def fetch_attendance(device):
	attendances = []
	conn = None
	try:
		conn = sync_device(ip = device.ip)
		if conn:
			x = conn.disable_device()
			info_logger.info("\t".join((device.ip, "Device Disable Attempted. Result:", str(x))))
			attendances = conn.get_attendance()
			info_logger.info("\t".join((device.ip, "Attendances Fetched:", str(len(attendances)))))
			status.set(f'{device.device_id}_push_timestamp', None)
			status.set(f'{device.device_id}_pull_timestamp', str(datetime.datetime.now()))
			if len(attendances):
				dump_file_name = logs_directory+'/' + device.device_id + "_" + device.ip.replace('.', '_') + '_last_fetch_dump.json'
				with open(dump_file_name, 'w+') as f:
					f.write(json.dumps(list(map(lambda x: x.__dict__, attendances)), default=datetime.datetime.timestamp))
				if device.clear_from_device_on_fetch:
					x = conn.clear_attendance()
					info_logger.info("\t".join((device.ip, "Attendance Clear Attempted. Result:", str(x))))
			x = conn.enable_device()
			info_logger.info("\t".join((device.ip, "Device Enable Attempted. Result:", str(x))))
	except:
		error_logger.exception(str(device.ip)+' exception when fetching from device...')
		raise Exception('Device fetch failed.')
	finally:
		if conn:
			conn.disconnect()
	return list(map(lambda x: x.__dict__, attendances))

def shift_type_device_map(device_details):
	shift_type_device_mapping = []
	shift_type_list = frappe.get_all('Shift Type')
	device_list= []
	for device in device_details:
		device_list.append(device.device_id)
	for shift_type in shift_type_list:
		mapped_devices = frappe.get_list('Combined Shift Type',
					{'shift_type':shift_type['name'],'parent':['in',device_list]},'parent') 
		related_device_id = [data['parent'] for data in mapped_devices]
		if related_device_id:
			shift_type_device_mapping.append({'shift_type_name': [shift_type['name']],
					'related_device_id': related_device_id})
	return shift_type_device_mapping

def update_shift_last_sync_timestamp(shift_type_device_mapping):
	for shift_type_device_map in shift_type_device_mapping:
		all_devices_pushed = True
		pull_timestamp_array = []
		for device_id in shift_type_device_map['related_device_id']:
			if not status.get(f'{device_id}_push_timestamp'):
				all_devices_pushed = False
				break
			pull_timestamp_array.append(_safe_convert_date(status.get(f'{device_id}_pull_timestamp'), "%Y-%m-%d %H:%M:%S.%f"))
		if all_devices_pushed:
			min_pull_timestamp = min(pull_timestamp_array)
			if isinstance(shift_type_device_map['shift_type_name'], str): 
				shift_type_device_map['shift_type_name'] = [shift_type_device_map['shift_type_name']]
			for shift in shift_type_device_map['shift_type_name']:
				try:
					sync_current_timestamp = _safe_convert_date(status.get(f'{shift}_sync_timestamp'), "%Y-%m-%d %H:%M:%S.%f")
					if (sync_current_timestamp and min_pull_timestamp > sync_current_timestamp) or (min_pull_timestamp and not sync_current_timestamp):
						frappe.db.sql("""update `tabShift Type`
							set last_sync_of_checkin = %s
							where name = %s""", (str(min_pull_timestamp), shift))
				except:
					error_logger.exception('Exception in update_shift_last_sync_timestamp, for shift:'+shift)

def get_last_line_from_file(file):
	# concerns to address(may be much later):
		# how will last line lookup work with log rotation when a new file is created?
			#- will that new file be empty at any time? or will it have a partial line from the previous file?
	line = None
	if os.stat(file).st_size < 5000:
		# quick hack to handle files with one line
		with open(file, 'r') as f:
			for line in f:
				pass
	else:
		# optimized for large log files
		with open(file, 'rb') as f:
			f.seek(-2, os.SEEK_END)
			while f.read(1) != b'\n':
				f.seek(-2, os.SEEK_CUR)
			line = f.readline().decode()
	return line

def _apply_function_to_key(obj, key, fn):
	obj[key] = fn(obj[key])
	return obj

def _safe_convert_date(datestring, pattern):
	try:
		return datetime.datetime.strptime(datestring, pattern)
	except:
		return None