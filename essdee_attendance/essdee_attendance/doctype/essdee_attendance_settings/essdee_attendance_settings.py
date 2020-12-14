# -*- coding: utf-8 -*-
# Copyright (c) 2020, Aerele and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.model.document import Document
from frappe.utils import cint, flt, nowdate, getdate, add_days
from datetime import timedelta, datetime

class EssdeeAttendanceSettings(Document):
	pass

def make_custom_field():
	custom_fields = {
		'Employee': [
		{
			"fieldname": "rate",
			"fieldtype": "Currency",
			"label": "Rate",
			"description": "Allocate rate per shift",
			"insert_after": "date_of_joining",
			"reqd": 1,
			"precision": 2
			}		
		],
		'Attendance': [
			{
			"fieldname": "no_of_shifts",
			"fieldtype": "Float",
			"label": "No of Shifts",
			"insert_after": "shift",
			"reqd": 1,
			"precision": 2
			}	
		],
		'Shift Type': [
			{
			"fieldname": "enable_essdee_auto_attendance",
			"fieldtype": "Check",
			"label": "Enable Essdee Auto Attendance",
			"insert_after": "enable_auto_attendance"
			},
			{
			"fieldname": "essdee_attendance_settings",
 			"label": "Essdee Attendance Settings",
 			"fieldtype": 'Section Break',
			"insert_after": "enable_essdee_auto_attendance",
 			"depends_on": "enable_essdee_auto_attendance"
			},
			{
			"fieldname": "shift_time_mapping",
			"fieldtype": "Table",
			"label": "Shift Time Mapping",
			"options": "Shift Time Mapping",
			"insert_after": "essdee_attendance_settings"
			},
			{
			"fieldname": "allowed_early_entry",
			"fieldtype": "Int",
			"label": "Allowed Early Entry (In Mins)",
			"insert_after": "shift_time_mapping",
			"default": 30
			},
			{
			"fieldname": "allowed_late_entry",
			"fieldtype": "Int",
			"label": "Allowed Late Entry (In Mins)",
			"insert_after": "allowed_early_entry",
			"default": 30
			}
		]
	}
	create_custom_fields(custom_fields, ignore_validate=frappe.flags.in_patch, update=True)

@frappe.whitelist()
def mark_attendance():
	employees = frappe.get_all('Employee',  fields=['name', 'default_shift', 'company'])
	for employee in employees:
		shift_doc = frappe.get_doc('Shift Type', employee['default_shift'])
		if cint(shift_doc.enable_essdee_auto_attendance):
			filters = {
				'skip_auto_attendance':'0',
				'attendance':('is', 'not set'),
				'time':("Between", [nowdate(), nowdate()]),
				'employee': employee['name'],
				'log_type': 'IN'
			}
			logs = frappe.db.get_list('Employee Checkin', fields="*", filters=filters, order_by="time")
			log_names, total_shift = calculate_total_shift(shift_doc, logs)
			existing_attendance = frappe.db.get_value('Attendance', {'employee':employee['name'], 'attendance_date':nowdate()})
			if not existing_attendance:
				doc_dict = {
					'doctype': 'Attendance',
					'employee': employee['name'],
					'attendance_date': nowdate(),
					'status': 'Present' if total_shift else 'Absent',
					'no_of_shifts': total_shift,
					'company': employee['company'],
					'shift': employee['default_shift']
				}
				attendance = frappe.get_doc(doc_dict).insert()
				attendance.save()
				existing_attendance = attendance.name
			else:
				doc = frappe.get_doc('Attendance', existing_attendance)
				if doc.docstatus == 0:
					doc.status = 'Present' if total_shift else 'Absent'
					doc.no_of_shifts = flt(doc.no_of_shifts) + total_shift
					doc.save()
			if log_names:
				frappe.db.sql("""update `tabEmployee Checkin`
						set attendance = %s
						where name in %s""", (existing_attendance, log_names))

def calculate_total_shift(shift_doc, logs):
	total_shift = 0
	log_names = []
	if logs:
		for row in shift_doc.shift_time_mapping:
			in_log = []
			for log in logs:
				if log['time'].time() <= (datetime.combine(getdate(nowdate()), datetime.min.time()) + (row.in_time + timedelta(minutes = shift_doc.allowed_early_entry))).time() and log['time'].time() >= (datetime.combine(getdate(nowdate()), datetime.min.time()) + (row.in_time - timedelta(minutes = shift_doc.allowed_early_entry))).time():
					in_log.append(log)
			if in_log:
				total_shift += row.shift
				log_names.append(in_log[0]['name'])
	return log_names, total_shift

def submit_all_record():
	non_submitted_records = frappe.get_all('Attendance', {'attendance_date':add_days(getdate(nowdate()), -1), 'docstatus':('=', '0')})
	for record in non_submitted_records:
		doc = frappe.get_doc('Attendance', record['name'])
		doc.submit()