# Copyright (c) 2024, Aerele and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_columns():
	return [
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
			"width": 120,
		},
		{
			"label": _("Employee Name"),
			"fieldname": "employee_name",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("Bank A/C No."),
			"fieldname": "bank_ac_no",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("IFSC Code"),
			"fieldname": "ifsc_code",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("Total Amount"),
			"fieldname": "total_amount",
			"fieldtype": "currency",
			"width": 120,
		},
		{
			"label": _("Salary Mode"),
			"fieldname": "salary_mode",
			"fieldtype": "Data",
			"width": 120,
		},
		{
			"label": _("Salary Slip"),
			"fieldname": "salary_slip_name",
			"fieldtype": "Link",
			"options": "SD Salary Slip",
			"width": 120,
		},
		{
			"label": _("Salary Slip Date"),
			"fieldname": "salary_slip_date",
			"fieldtype": "Date",
			"width": 120,
		},
	]

def get_data(filters):
	SalarySlip = frappe.qb.DocType("SD Salary Slip")
	Employee = frappe.qb.DocType("Employee")

	q = (
		frappe.qb.from_(SalarySlip)
		.left_join(Employee).on(Employee.name == SalarySlip.employee)
		.select(
			Employee.sd_attendance_book_serial.as_("serial"),
			Employee.name.as_("employee"),
			Employee.employee_name,
			Employee.bank_ac_no,
			Employee.ifsc_code,
			Employee.salary_mode,
			SalarySlip.total_amount,
			SalarySlip.name.as_("salary_slip_name"),
			SalarySlip.date.as_("salary_slip_date"),
		)
	)
	if filters:
		if filters.get('from_date'):
			q = q.where(SalarySlip.date >= filters.get('from_date'))
		if filters.get('to_date'):
			q = q.where(SalarySlip.date <= filters.get('to_date'))
		if filters.get('employee'):
			q = q.where(Employee.name == filters.get('employee'))
		if filters.get('department'):
			q = q.where(Employee.department == filters.get('department'))
		if filters.get('employment_type'):
			q = q.where(Employee.employment_type == filters.get('employment_type'))
		if filters.get('designation'):
			q = q.where(Employee.designation == filters.get('designation'))
		if filters.get('branch'):
			q = q.where(Employee.branch == filters.get('branch'))
		if filters.get('salary_mode'):
			q = q.where(Employee.salary_mode == filters.get('salary_mode'))
	
	q = q.where(Employee.status == 'Active')
	q = q.orderby(Employee.sd_attendance_book_serial.isnull())
	q = q.orderby(Employee.sd_attendance_book_serial)
	q = q.orderby(Employee.name)

	data = q.run(as_dict=True)
	validate_duplicate(data)
	return data

def validate_duplicate(salary_slips):
	emps = []
	duplicates = set()
	for slip in salary_slips:
		if slip.employee in emps:
			duplicates.add(slip.employee)
		else:
			emps.append(slip.employee)
	duplicates = list(duplicates)
	if duplicates:
		frappe.throw(f"There are more than one entry for the below employees in this date range<br>{'<br>'.join(duplicates)}")
