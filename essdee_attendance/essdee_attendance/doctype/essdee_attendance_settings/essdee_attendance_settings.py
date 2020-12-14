# -*- coding: utf-8 -*-
# Copyright (c) 2020, Aerele and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.model.document import Document

class EssdeeAttendanceSettings(Document):
	pass

def make_custom_field():
	custom_fields = {
		'Employee': [
		{
			"fieldname": "rate",
			"fieldtype": "Int",
			"label": "Rate",
			"description": "Allocate rate per shift",
			"insert_after": "date_of_joining",
			"reqd": 1
			}		
		],
		'Attendance': [
			{
			"fieldname": "no_of_shifts",
			"fieldtype": "Int",
			"label": "No of Shifts",
			"insert_after": "shift",
			"reqd": 1
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