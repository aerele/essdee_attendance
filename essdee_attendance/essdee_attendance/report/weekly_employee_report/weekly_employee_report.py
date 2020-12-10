# Copyright (c) 2013, Aerele and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

default_hour_per_shift = frappe.db.get_single_value('Essdee Attendance Settings', 'no_of_hours')

def execute(filters=None):
	columns, data = [], []
	if filters:
		columns = get_columns()
		get_data(filters, data)
	return columns, data

def get_columns():
	return [
		_("Employee") + ":Link/Employee:120",
		_("Name") + ":Data:200",
		_("Shift") + ":Float:100",
		_("Rate") + ":Currency:70",
		_("Amount") + ":Currency:150"
	]

def get_data(filters, data):
	if 'employee' in filters:
		employee_details = frappe.db.get_values('Employee',filters['employee'],fieldname=['name', 'employee_name','rate'], as_dict=True)
	else:
		employee_details = frappe.get_all("Employee",fields=['name', 'employee_name','rate'])
	for employee_detail in employee_details:
		if frappe.db.exists("Attendance", {'employee':employee_detail['name']}):
			data.append(get_employee_specific_data(employee_detail, filters))
	return data


def get_employee_specific_data(employee_detail, filters):
	working_hours = frappe.get_list('Attendance',{'attendance_date':('between',[filters['from_date'],filters['to_date']]),'employee':employee_detail['name']}, ['working_hours'], as_list = True)
	if working_hours:
		total_shift = sum([hour[0] for hour in working_hours ]) / default_hour_per_shift
		if total_shift:
			return {
				'employee': employee_detail['name'],
				'name': employee_detail['employee_name'],
				'shift': total_shift,
				'rate': employee_detail['rate'],
				'amount': total_shift * employee_detail['rate']}