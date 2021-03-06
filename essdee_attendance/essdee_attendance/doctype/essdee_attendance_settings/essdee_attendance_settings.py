# -*- coding: utf-8 -*-
# Copyright (c) 2020, Aerele and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.model.document import Document
from frappe.utils import cint, nowdate, getdate
from datetime import timedelta, datetime
from frappe.core.page.background_jobs.background_jobs import get_info
from frappe.utils.background_jobs import enqueue
from zk import ZK
from frappe import _, msgprint
from six import string_types
from itertools import groupby
import codecs
from operator import itemgetter

class EssdeeAttendanceSettings(Document):
	pass

def make_custom_field():
	custom_fields = {
		'Employee': [
			{
			"fieldname": "sd_shift_rate",
			"fieldtype": "Currency",
			"label": "Shift Rate",
			"description": "Allocate rate per shift",
			"insert_after": "date_of_joining",
			"reqd": 1,
			"precision": 2
			},
			{
			"fieldname": "work_location",
			"fieldtype": "Table",
			"label": "Work Location",
			"options": "Work Location",
			"insert_after": "attendance_device_id"
			},
			{
			"fieldname": "finger_print_details",
			"fieldtype": "Table",
			"label": "Finger Print Details",
			"options": "Finger Print Details",
			"insert_after": "work_location",
			"read_only": 1
			},
			{
			"fieldname": "enroll_fingerprint",
			"depends_on": "eval: !doc.__islocal",
			"fieldtype": "Button",
			"label": "Enroll Fingerprint",
			"insert_after": "default_shift"
			},
			{
			"fieldname": "sync_now",
			"depends_on": "eval: !doc.__islocal",
			"fieldtype": "Button",
			"label": "Sync Now",
			"insert_after": "enroll_fingerprint"
			}		
		],
		'Attendance': [
			{
			"fieldname": "sd_no_of_shifts",
			"fieldtype": "Float",
			"label": "No of Shifts",
			"insert_after": "shift",
			"reqd": 1,
			"precision": 2
			}	
		],
		'Shift Type': [
			{
			"fieldname": "sd_enable_essdee_attendance",
			"fieldtype": "Check",
			"label": "Enable Essdee Attendance",
			"insert_after": "enable_auto_attendance"
			},
			{
			"fieldname": "sd_essdee_attendance_settings",
 			"label": "Essdee Attendance Settings",
 			"fieldtype": 'Section Break',
			"insert_after": "sd_enable_essdee_attendance",
 			"depends_on": "sd_enable_essdee_attendance"
			},
			{
			"fieldname": "sd_shift_time_mapping",
			"fieldtype": "Table",
			"label": "Shift Time Mapping",
			"options": "Shift Time Mapping",
			"insert_after": "sd_essdee_attendance_settings"
			}
		]
	}
	create_custom_fields(custom_fields, ignore_validate=frappe.flags.in_patch, update=True)

def update_attendance():
	enabled = frappe.db.get_single_value('Essdee Attendance Settings', 'update_shift_daily')
	if enabled:
		update_shift_to_attendance()
	else:
		frappe.log_error(
			_("Daily update of shifts to the attendance is not enabled in essdee attendance settings")
		)

@frappe.whitelist()
def update_shift_to_attendance():
	employees = frappe.get_all('Employee',  fields=['name', 'default_shift', 'company'])
	for employee in employees:
		attendance_list = frappe.db.get_list('Attendance', {'employee':employee['name'], \
				'docstatus': 1, 'sd_no_of_shifts': '0.00', 'status': 'Present'}, order_by="attendance_date")
		shift_doc = frappe.get_doc('Shift Type', employee['default_shift'])
		for attendance in attendance_list:
			if cint(shift_doc.sd_enable_essdee_attendance):
				filters = {
					'attendance': attendance['name'],
					'employee': employee['name'],
					'log_type': 'IN'
				}
				logs = frappe.db.get_list('Employee Checkin', fields="*", filters=filters, order_by="time")
				total_shift = calculate_total_shift(shift_doc, logs)
				if total_shift:
					frappe.db.sql("""update `tabAttendance`
							set sd_no_of_shifts = %s
							where name = %s""", (total_shift, attendance['name']))

def calculate_total_shift(shift_doc, logs):
	total_shift = 0
	if logs:
		for row in shift_doc.sd_shift_time_mapping:
			in_log = []
			late_entry = datetime.combine(getdate(nowdate()), datetime.min.time()) \
				 + (row.in_time + timedelta(minutes = row.allowed_late_entry))
			early_entry = datetime.combine(getdate(nowdate()), datetime.min.time()) \
				+ (row.in_time - timedelta(minutes = row.allowed_early_entry))
			for log in logs:
				if log['time'].time() <=  late_entry.time() \
					and log['time'].time() >= early_entry.time():
					in_log.append(log)
			if in_log:
				total_shift += row.shift
	return total_shift

def sync_device(ip, port=4370, timeout=30):
	zk = ZK(ip, port=port, timeout=timeout)
	conn = zk.connect()
	return conn

@frappe.whitelist()
def enroll_fingerprint(doc, device):
	if isinstance(doc, string_types):
		doc = frappe._dict(json.loads(doc))
	try:
		device_doc = frappe.get_doc('Essdee Biometric Device', device)
		conn = sync_device(ip = device_doc.ip)
		if conn:
			uid = int(doc.attendance_device_id)
			conn.set_user(uid= uid, name= doc.employee_name, user_id= doc.attendance_device_id)
			temp_id = len(doc.finger_print_details)
			enrolled = conn.enroll_user(uid, temp_id)
			if enrolled:
				template_obj = conn.get_user_template(uid, temp_id)
				template = json_pack(template_obj)
				doc = frappe.get_doc('Employee', doc.name)
				if template['valid']:
					template['fid'] = 'FID '+str(template['fid'])
					is_exist = frappe.db.get_value('Finger Print Details', {'parent': doc.name, "id":template['fid']})
					if not is_exist:
						return template['fid'], template['template']
				conn.disconnect()
			else:
				frappe.throw(_('Please Try Again'))
	except Exception as e:
		raise e

def json_pack(data):
	return {
		"size": data.size,
		"uid": data.uid,
		"fid": data.fid,
		"valid": data.valid,
		"template": codecs.encode(data.template, 'hex').decode('ascii')
	}

def update_attendance_device_id(doc, action):
	if action == 'after_insert':
		last_device_id = 1
		employee_list = frappe.get_all('Employee', ['attendance_device_id'], order_by="creation DESC")
		if employee_list and len(employee_list) > 1:
			last_device_id = int(employee_list[1]['attendance_device_id'])
			last_device_id +=1
		doc.attendance_device_id = last_device_id
		doc.save()

@frappe.whitelist()
def sync_now(device=None, location=None, employee=None):
	if device:
		if isinstance(device, string_types):
			device = frappe._dict(json.loads(device))
		employee_list = frappe.get_all('Work Location', {'sd_location': device.location}, 'parent')
		employee_id_list = [int(frappe.db.get_value('Employee', emp['parent'], 'attendance_device_id')) for emp in employee_list]
		device_list = [device.name]
		if not device_list:
			frappe.throw("No employee found for this device location {device.location}")

	if location:
		if isinstance(location, string_types):
			location = frappe._dict(json.loads(location))
		device_list = frappe.get_all('Essdee Biometric Device', {'location': location.name}, 'name')
		employee_list = frappe.get_all('Work Location', {'sd_location': location.name}, 'parent')
		employee_id_list = [int(frappe.db.get_value('Employee', emp['parent'], 'attendance_device_id')) for emp in employee_list]
		device_list = [device['name'] for device in device_list]
		if not device_list:
			frappe.throw(f"No device linked to this location {location.name}")

		if not employee_list:
			frappe.throw(f"No employee linked to this location {location.name}")		

	if employee:
		if isinstance(employee, string_types):
			employee = frappe._dict(json.loads(employee))
		location_list = frappe.get_all('Work Location', {'parent': employee.name}, 'sd_location')
		location_list = [location['sd_location'] for location in location_list]
		device_list = frappe.get_all('Essdee Biometric Device', {'location': ['in', location_list]}, 'name')
		device_list = [device['name'] for device in device_list]
		employee_id_list = [int(employee.attendance_device_id)]
		if not device_list:
			frappe.throw(f"No device location linked to the employee {employee.name}")

	info = {'employee_id_list': employee_id_list, 'device_list': device_list}
	compare_records(info)

def compare_records(info):
	for device in info['device_list']:
		device_ip = frappe.db.get_value('Essdee Biometric Device', device, 'ip')
		conn = None
		try:
			conn = sync_device(device_ip, port=4370, timeout=30)
			if not conn:
				frappe.throw(f'Unable to sync device {device}')
			conn.disable_device()
			users = conn.get_users()
			templates = conn.get_templates()
			conn.enable_device()
			mismatched_users = []
			templates = [json_pack(t) for t in templates]
			users = [u.__dict__ for u in users]
			user_id_list = [u['uid'] for u in users]
			sync_status = 0
			if users:
				diff_list = list(set(info['employee_id_list']) - set(user_id_list))
				for user in users:
					employee = frappe.db.get_value('Employee', {'attendance_device_id': user['uid']}, 'name')
					if not user['uid'] in info['employee_id_list']:
						mismatched_users.append(user)
						continue
					if templates and employee:
						doc = frappe.get_doc('Employee', employee)
						if doc.employee_name != user['name']:
							sync_status = 1
							create_sync_records(user['uid'], device_ip, 'Update')
						
						fid_key = itemgetter('fid')
						user_templates = ['FID '+ str(x["fid"]) for x in templates if x["uid"] == int(doc.attendance_device_id)]
						if doc.finger_print_details:
							for row in doc.finger_print_details:		
								if row.id not in user_templates:
									sync_status = 1
									create_sync_records(user['uid'], device_ip, 'Sync Templates')
									break
				if diff_list:
					for id in diff_list:
						create_sync_records(id, device_ip, 'All')
					sync_status = 1
			else:
				for id in info['employee_id_list']:
					create_sync_records(id, device_ip, 'All')
				sync_status = 1

			if mismatched_users:
				frappe.log_error(title='Employee not found', message=f'Employee not found for the device users{mismatched_users}')
				msgprint('Employee not found for some device users. Check error log for more info')
			
			if sync_status:
				msgprint('Sync on progress. Please check status in sync log after sometimes.')
			else:
				msgprint('Already Synced')
		except:
			frappe.throw(frappe.get_traceback())
		finally:
			if conn:
				conn.disconnect()

def create_sync_records(id, device_ip, action):
	id = frappe.db.get_value('Employee',{'attendance_device_id':id},'name')
	is_exist = frappe.db.get_value('Essdee Biometric Device Sync Log',
		{'employee': id,
		'device_ip': device_ip,
		'action': action,
		'status': ['in',['Error', 'Queued']],
		'resend_count': ['<', 5]})
	if not is_exist:
		frappe.get_doc({'doctype': 'Essdee Biometric Device Sync Log',
			'employee': id,
			'device_ip': device_ip,
			'action': action,
			'status': 'Queued'}).save()

def validate_location(doc, action):
	if action == 'before_save':
		previous_locations = [loc['sd_location'] for loc in frappe.get_all('Work Location', {'parent': doc.name}, ['sd_location'])]
		if previous_locations and not doc.work_location:
			previous_locations = previous_locations
		if doc.work_location and previous_locations:
			for loc in doc.work_location:
				if loc.sd_location in previous_locations:
					previous_locations.remove(loc.sd_location)
		if previous_locations:
			ip_list = frappe.db.get_all('Essdee Biometric Device', {'location': ['in', previous_locations]}, 'ip')
			for ip in ip_list:
				create_sync_records(doc.attendance_device_id, ip['ip'], 'Delete')