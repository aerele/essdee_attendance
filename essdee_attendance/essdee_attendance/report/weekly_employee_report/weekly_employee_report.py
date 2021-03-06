# Copyright (c) 2013, Aerele and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import add_days, getdate, cstr

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
		columns = get_columns(filters, columns)
		data = get_data(filters, data)
	return columns, data

def get_columns(filters, columns):
	columns += [
		_("Employee") + ":Link/Employee:120", _("Employee Name") + ":Data/:120"
	]
	week_date_list = []
	from_date = getdate(filters['from_date'])
	to_date = getdate(filters['to_date'])
	date_range = (to_date - from_date).days
	for idx in range(date_range+1):
		day_name = day_abbr[from_date.weekday()]
		week_date_list.append(cstr(from_date.strftime("%d-%m-%Y"))+ " " +day_name +"::120")
		from_date = add_days(from_date, 1)
	if not filters.summarized_view or filters.show_time_logs:
		columns += week_date_list
	if filters.summarized_view:
		columns += [
			_("Total Shift") + ":Float:100",
			_("Rate") + ":Currency:70",
			_("Amount") + ":Currency:150"
		]
	if filters.summarized_view and filters.show_time_logs:
		columns = []
	return columns

def get_data(filters, data):
	if filters.summarized_view and filters.show_time_logs:
		return []
	if 'employee' in filters:
		employee_details = frappe.db.get_values('Employee',filters['employee'], \
			fieldname=['name', 'employee_name','sd_shift_rate'], as_dict=True)
	else:
		employee_details = frappe.get_all("Employee",fields=['name', 'employee_name','sd_shift_rate'])
	for employee_detail in employee_details:
		if frappe.db.exists("Attendance", {'employee':employee_detail['name'], 'status':'Present', 'docstatus': 1}):
			data.append(get_employee_specific_data(employee_detail, filters))
	return data


def get_employee_specific_data(employee_detail, filters):
	if filters.summarized_view:
		shifts = frappe.get_list('Attendance',{'attendance_date':('between',[filters['from_date'],filters['to_date']]), \
			'employee':employee_detail['name'], 'status':'Present', 'docstatus': 1}, ['sd_no_of_shifts'], as_list = True)
		total_shift = sum([float(shift[0]) for shift in shifts if shift[0]])
		return {
			'employee': employee_detail['name'],
			'employee_name': employee_detail['employee_name'],
			'total_shift': total_shift,
			'rate': employee_detail['sd_shift_rate'],
			'amount': total_shift * employee_detail['sd_shift_rate']}
	else:
		from_date = getdate(filters['from_date'])
		to_date = getdate(filters['to_date'])
		date_range = (to_date - from_date).days
		data = [employee_detail['name'],employee_detail['employee_name']]
		for idx in range(date_range+1):
			if filters.show_time_logs:
				time_log = ''
				attendance = frappe.db.get_value('Attendance',{'attendance_date': from_date, \
					'employee':employee_detail['name'], 'status':'Present', 'docstatus': 1})
				if attendance:
					employee_checkin_list = frappe.get_list('Employee Checkin',{'attendance':attendance},'time')
					time_log = ', '.join([data['time'].strftime("%H:%M") for data in employee_checkin_list])
				data.append(time_log)
			else:
				shift = frappe.db.get_value('Attendance',{'attendance_date': from_date, \
					'employee':employee_detail['name'], 'status':'Present', 'docstatus': 1}, ['sd_no_of_shifts'])
				data.append(shift if shift else 0)
			from_date = add_days(from_date, 1)
		return data