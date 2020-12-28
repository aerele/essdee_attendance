# -*- coding: utf-8 -*-
# Copyright (c) 2020, Aerele and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.model.document import Document
from frappe.utils import cint, nowdate, getdate
from datetime import timedelta, datetime
from frappe.core.page.background_jobs.background_jobs import get_info
from frappe.utils.background_jobs import enqueue
from zk import ZK
from frappe import _, msgprint

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

@frappe.whitelist()
def update_attendance():
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
def sync_now():
	enqueued_jobs = [d.get("job_name") for d in get_info()]
	if 'sync employees' in enqueued_jobs:
		frappe.throw(
			_("Sync already in progress. Please wait for sometime.")
		)
	else:
		enqueue(
			sync_all_employees,
			queue="default",
			timeout=6000,
			event="sync_employee_record",
			job_name='sync employees'
		)
		frappe.throw(
			_("Sync job added to queue. Please check after sometime.")
		)

def sync_all_employees():
	try:
		employee_record = frappe.get_all('Employee',{'name','employee_name'})
		settings = frappe.get_single('Essdee Attendance Settings')
		for device in settings.device_details:
			conn = sync_device(ip = device.ip)
			if conn:
				for record in employee_record:
					conn.set_user(uid= record['name'], name= record['employee_name'], user_id= record['name'])
				conn.disconnect()
	except:
		error_message = frappe.get_traceback()
		frappe.log_error(error_message, "Employee Records Sync Error")
		raise

@frappe.whitelist()
def delete_employee(employee):
	try:
		settings = frappe.get_single('Essdee Attendance Settings')
		for device in settings.device_details:
			conn = sync_device(ip = device.ip)
			if conn:
				conn.delete_user(uid= employee)
				conn.disconnect()
		msgprint(_('Successfully deleted the linked user'))
	except Exception as e:
		raise e