# Copyright (c) 2013, Aerele and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import getdate, add_days, cstr, get_datetime

day_abbr = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

def execute(filters=None):
	filters = frappe._dict(filters or {})
	columns, data = [], []
	if not filters.from_date or not filters.to_date:
		frappe.throw("Set Date Range")
	
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data
	
def get_columns(filters):
	columns = [
		{
			"label": _("Serial No."),
			"fieldname": "serial",
			"fieldtype": "data",
			"width": 115,
		},
		{
			"label": _("Employee"),
			"fieldname": "employee",
			"fieldtype": "Link",
			"options": "Employee",
			"width": 115,
		},
		{"label": _("Employee Name"), "fieldname": "employee_name", "fieldtype": "Data", "width": 120},
	]
	if filters.pf_view:
		columns.extend([
			{"label": _("Shift"), "fieldname": "shift", "fieldtype": "Data", "width": 65},
			{"label": _("No. of Shifts"), "fieldname": "shift_count", "fieldtype": "Float", "width": 120},
			{"label": _("Rate"), "fieldname": "rate", "fieldtype": "Float", "width": 120},
			{"label": _("Amount"), "fieldname": "amount", "fieldtype": "Float", "width": 120},
			{"label": _("General Shift"), "fieldname": "general_shifts", "fieldtype": "Float", "width": 120},
			{"label": _("OT Shift"), "fieldname": "ot_shifts", "fieldtype": "Float", "width": 120},
			{"label": _("PF Rate"), "fieldname": "pf_rate", "fieldtype": "Float", "width": 120},
			{"label": _("PF Amount"), "fieldname": "pf_amount", "fieldtype": "Float", "width": 120},
			{"label":_("HRA Rate"),"fieldname":"hra_rate","fieldtype":"Currency","width":100},
			{"label":_("PF Salary"),"fieldname":"pf_salary","fieldtype":"Currency","width":100},
			{"label":_("HRA"),"fieldname":"hra","fieldtype":"Currency","width":100},
			{"label":_("ESI Salary"),"fieldname":"esi_salary","fieldtype":"Currency","width":100},
			{"label":_("PF"),"fieldname":"pf","fieldtype":"Currency","width":100},
			{"label":_("ESI"),"fieldname":"esi","fieldtype":"Currency","width":100},
			{"label":_("Other Deductions"),"fieldname":"other_deductions","fieldtype":"Currency","width":100},
			{"label":_("Deductions"),"fieldname":"deductions","fieldtype":"Currency","width":100},
			{"label":_("Net Salary"),"fieldname":"net_salary","fieldtype":"Currency","width":100},
		])
	elif filters.select == "Summarized Report":
		columns.extend([
			{"label": _("Shift"), "fieldname": "shift", "fieldtype": "Data", "width": 65},
			{"label": _("No. of Shifts"), "fieldname": "shift_count", "fieldtype": "Float", "width": 120},
			{"label": _("Rate"), "fieldname": "rate", "fieldtype": "Float", "width": 120},
			{"label": _("Amount"), "fieldname": "amount", "fieldtype": "Float", "width": 120},
		])
	else:
		columns.extend(get_columns_for_days(filters))	
	return columns

def get_columns_for_days(filters):
	days = []
	date = getdate(filters.from_date)
	to_date = getdate(filters.to_date)
	
	while date <= to_date:
		weekday = day_abbr[date.weekday()]
		label = "{} {}".format(cstr(date.day), weekday)
		days.append({"label": label, "fieldtype": "Data", "fieldname": date.isoformat(), "width": 145})
		date = add_days(date, 1)
	return days

def get_data(filters):
	data = []
	employees = get_employees(filters)
	attendance_records = get_attendance_map(filters)
	attendance_records = get_checkin_map(attendance_records, filters)
	for employee in employees:
		d = {
			'serial': employee.serial,
			'employee': employee.name,
			'employee_name': employee.employee_name
		}
		if filters.pf_view:
			get_pf_detail(d, filters, employee, attendance_records.get(employee.name))
		elif filters.select == "Summarized Report":
			get_summarized_detail(d, filters, employee, attendance_records.get(employee.name))
		elif filters.select == "Day Wise Report":
			get_employee_detail(d, filters, employee, attendance_records.get(employee.name))	
		data.append(d)
	return data

def get_summarized_detail(data, filters, employee, attendance_records):
	if attendance_records:
		total_shift = 0
		for date, value in attendance_records.items():
			total_shift += (value.get('sd_no_of_shifts') or 0)
		data.update({
			'shift_count': total_shift,
			'rate': employee.sd_shift_rate,
			'amount': total_shift * (employee.sd_shift_rate or 0)
		})

def get_pf_detail(data, filters, employee, attendance_records):
	if attendance_records:
		general_shift = 0
		ot_shift = 0
		no_of_shifts = 0
		for date, value in attendance_records.items():
			no_of_shifts += (value.get('sd_no_of_shifts') or 0)
			general_shift += (value.get('general_shifts') or 0)
			ot_shift += (value.get('ot_shifts') or 0)
		total_shift = general_shift + ot_shift
		hra_rate = employee.sd_shift_wages - employee.sd_shift_rate
		pf_salary = employee.sd_shift_rate * general_shift
		hra = total_shift * hra_rate
		esi_salary = pf_salary + hra
		pf = pf_salary * 0.12
		esi = esi_salary * 0.75
		esi = esi/ 100
		old_total = no_of_shifts * (employee.sd_shift_rate or 0)
		new_total = total_shift * (employee.sd_shift_wages or 0)
		other_deductions = new_total - old_total
		deductions = pf + esi + other_deductions
		net_salary = new_total - deductions

		data.update({
			"shift_count":no_of_shifts,
			"rate":employee.sd_shift_rate,
			"amount":old_total,
			'general_shifts': general_shift,
			'ot_shifts':ot_shift,
			"pf_rate": employee.sd_shift_wages,
			'pf_amount': new_total,
			"hra_rate":hra_rate,
			"pf_salary":pf_salary,
			"hra":hra,
			"esi_salary":esi_salary,
			"pf":pf,
			"esi":esi,
			"other_deductions":other_deductions,
			"deductions":deductions,
			"net_salary":net_salary
		})

def get_employee_detail(data, filters, employee, attendance_records):
	if attendance_records:
		for date, value in attendance_records.items():
			detail = []
			if filters.show_in_out:
				in_time = None
				out_time = None
				if value.get('in_time'):
					in_time = value['in_time'].strftime("%H:%M")
				if value.get('out_time'):
					out_time = value['out_time'].strftime("%H:%M")
				detail.append("{} - {}".format(in_time, out_time))
			if filters.show_time_logs:
				detail.append(", ".join(value.get('checkin') or []))
			if filters.show_hours:
				detail.append("{} - {} hrs".format(value.get('status') or '', value.get('working_hours') or 0))
			if filters.show_shift:
				detail.append(str(value.get('sd_no_of_shifts') or 0))
			if filters.show_general_ot_shift:
				str1 = str(value.get('general_shifts') or 0) 
				str2 = str(value.get('ot_shifts') or 0)
				str3 = str1 + "-" + str2
				detail.append(str3)
			data[date] = "<br>".join(detail)

def get_employees(filters):
	Employee = frappe.qb.DocType("Employee")
	
	query = frappe.qb.from_(Employee).select(Employee.sd_attendance_book_serial.as_("serial"),Employee.name, Employee.employee_name, Employee.sd_shift_rate, Employee.sd_shift_wages)
	query = apply_employee_filters(query, filters, Employee)
	query = query.orderby(Employee.sd_attendance_book_serial.isnull())
	query = query.orderby(Employee.sd_attendance_book_serial)
	return query.run(as_dict = 1)

def get_attendance_map(filters):
	attendance_list = get_attendance_records(filters)
	attendance_map = {}

	for d in attendance_list:
		attendance_map.setdefault(d.employee, {})
		attendance_map[d.employee][d.attendance_date.isoformat()] = {
			'employee_name': d.employee_name,
			'status': d.status,
			'shift': d.shift,
			'sd_no_of_shifts': d.sd_no_of_shifts,
			'in_time': d.in_time,
			'out_time': d.out_time,
			'working_hours': d.working_hours,
			'general_shifts': d.sd_general_shifts,
			'ot_shifts':d.sd_ot_shifts,
		}

	return attendance_map

def get_attendance_records(filters):
	Attendance = frappe.qb.DocType("Attendance")
	Employee = frappe.qb.DocType("Employee")
	
	query = (
		frappe.qb.from_(Attendance).from_(Employee)
		.select(
			Attendance.employee,
			Attendance.attendance_date,
			Attendance.status,
			Attendance.shift,
			Attendance.sd_no_of_shifts,
			Attendance.in_time,
			Attendance.out_time,
			Attendance.working_hours,
			Attendance.sd_general_shifts,
			Attendance.sd_ot_shifts,
		).where(
			(Attendance.docstatus == 1)
			& (Attendance.company == filters.company)
			& (Attendance.attendance_date >= filters.from_date)
			& (Attendance.attendance_date <= filters.to_date)
			& (Attendance.employee == Employee.name)
		)
	)

	query = apply_employee_filters(query, filters, Employee)
	query = query.orderby(Attendance.employee, Attendance.attendance_date)

	return query.run(as_dict=1)

def get_checkin_map(attendance_records, filters):
	if not filters.show_time_logs:
		return attendance_records
	checkin_list = get_check_in_records(filters)

	for d in checkin_list:
		date = getdate(d.time).isoformat()
		attendance_records.setdefault(d.employee, {}).setdefault(date, {}).setdefault('checkin', [])
		attendance_records[d.employee][date]['checkin'].append(d.time.strftime("%H:%M"))

	return attendance_records

def get_check_in_records(filters):
	EmployeeCheckin = frappe.qb.DocType("Employee Checkin")
	Employee = frappe.qb.DocType("Employee")
	
	query = (
		frappe.qb.from_(EmployeeCheckin).from_(Employee)
		.select(
			EmployeeCheckin.employee,
			EmployeeCheckin.time,
		).where(
			(EmployeeCheckin.attendance.notnull())
			& (EmployeeCheckin.time >= filters.from_date)
			& (EmployeeCheckin.time <= filters.to_date)
			& (EmployeeCheckin.employee == Employee.name)
		)
	)

	query = apply_employee_filters(query, filters, Employee)
	query = query.orderby(EmployeeCheckin.employee, EmployeeCheckin.time)

	return query.run(as_dict=1)

def apply_employee_filters(query, filters, Employee):
	if filters.employee:
		query = query.where(Employee.name == filters.employee)
	if filters.shift:
		query = query.where(Employee.default_shift == filters.shift)
	if filters.department:
		query = query.where(Employee.department == filters.department)
	if filters.branch:
		query = query.where(Employee.branch == filters.branch)
	if filters.employment_type:
		query = query.where(Employee.employment_type == filters.employment_type)
	if filters.status:
		if filters.status == "Active":
			query = query.where(Employee.status == "Active")
		else:
			query = query.where(Employee.status != "Active")
	return query
