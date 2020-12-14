# Copyright (c) 2013, Aerele and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import add_days, getdate, cstr

default_hour_per_shift = frappe.db.get_single_value('Essdee Attendance Settings', 'no_of_hours')

day_abbr = [
	"Mon",
	"Tue",
	"Wed",
	"Thu",
	"Fri",
	"Sat",
	"Sun"
]

def execute(filters=None):
	columns, data = [], []
	if filters:
		get_columns(filters, columns)
		get_data(filters, data)
	return columns, data

def get_columns(filters, columns):
	columns += [
		_("Employee") + ":Link/Employee:120", _("Employee Name") + ":Data/:120"
	]
	week_date_list = []
	from_date = getdate(filters['from_date'])
	to_date = getdate(filters['to_date'])
	date_range = (to_date - from_date).days
	for date in range(date_range+1):
		day_name = day_abbr[from_date.weekday()]
		week_date_list.append(cstr(from_date.strftime("%d-%m-%Y"))+ " " +day_name +"::120")
		from_date = add_days(from_date, 1)
	if not filters.summarized_view:
		columns += week_date_list
	else:
		columns += [
			_("Total Shift") + ":Float:100",
			_("Rate") + ":Currency:70",
			_("Amount") + ":Currency:150"
		]
	return columns

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
				'employee_name': employee_detail['employee_name'],
				'total_shift': total_shift,
				'rate': employee_detail['rate'],
				'amount': total_shift * employee_detail['rate']}