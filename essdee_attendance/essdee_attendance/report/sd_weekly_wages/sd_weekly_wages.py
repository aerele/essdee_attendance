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
		# {
		# 	"label": _("Serial No."),
		# 	"fieldname": "serial",
		# 	"fieldtype": "data",
		# 	"width": 115,
		# },
		{
			"label": _("Salary Batch"),
			"fieldname": "salary_batch",
			"fieldtype": "Link",
			"options": "SD Salary Batch",
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
			"label": _("Nick Name"),
			"fieldname": "nick_name",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("Shift Rate"),
			"fieldname": "shift_rate",
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"label": _("Department"),
			"fieldname": "department",
			"fieldtype": "Link",
			"options": "Department",
			"width": 120,
		},
		{
			"label": _("Employment Type"),
			"fieldname": "employment_type",
			"fieldtype": "Link",
			"options": "Employment Type",
			"width": 120,
		},
		{
			"label": _("Designation"),
			"fieldname": "designation",
			"fieldtype": "Link",
			"options": "Designation",
			"width": 120,
		},
		{
			"label": _("Branch"),
			"fieldname": "branch",
			"fieldtype": "Link",
			"options": "Branch",
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
			"label": _("Method"),
			"fieldname": "salary_slip_method",
			"fieldtype": "Data",
			"width": 120,
		},
		{
			"label": _("DocStatus"),
			"fieldname": "docstatus",
			"fieldtype": "Data",
			"width": 60,
		},
		{
			"label": _("Salary Slip Date"),
			"fieldname": "date",
			"fieldtype": "Date",
			"width": 120,
		},
		{
			"label": _("Salary Amount"),
			"fieldname": "salary_amount",
			"fieldtype": "currency",
			"width": 120,
		},
		{
			"label": _("Other Additions"),
			"fieldname": "other_additions",
			"fieldtype": "currency",
			"width": 120,
		},
		{
			"label": _("Canteen"),
			"fieldname": "canteen",
			"fieldtype": "currency",
			"width": 120,
		},
		{
			"label": _("Advance"),
			"fieldname": "advance",
			"fieldtype": "currency",
			"width": 120,
		},
		{
			"label": _("Leave"),
			"fieldname": "leave",
			"fieldtype": "currency",
			"width": 120,
		},
		{
			"label": _("ESI/PF"),
			"fieldname": "esi_pf",
			"fieldtype": "currency",
			"width": 120,
		},
		{
			"label": _("Via Cash"),
			"fieldname": "via_cash",
			"fieldtype": "currency",
			"width": 120,
		},
		{
			"label": _("Other Deductions"),
			"fieldname": "other_deductions",
			"fieldtype": "currency",
			"width": 120,
		},
		{
			"label": _("Total Deductions"),
			"fieldname": "total_deductions",
			"fieldtype": "currency",
			"width": 120,
		},
		{
			"label": _("Total Amount"),
			"fieldname": "total_amount",
			"fieldtype": "currency",
			"width": 120,
		},
		{
			"label": _("Previous Canteen"),
			"fieldname": "previous_canteen",
			"fieldtype": "currency",
			"width": 70
		},
		{
			"label": _("Status"),
			"fieldname": "status",
			"fieldtype": "Data",
			"width": 70
		},
		{
			"label":_("Worked Days"),
			"fieldname":"no_of_days_worked",
			"fieldtype":"Int",
			"width":100,
		},
		{
			"label": _("Current Advance Balance"),
			"fieldname": "current_advance_balance",
			"fieldtype": "Currency",
			"width": 120,
		},
	]

def get_all_active_employees(filters = None):
	Employee = frappe.qb.DocType("Employee")
	q = (
		frappe.qb.from_(Employee)
		.select(
			# Employee.sd_attendance_book_serial.as_("serial"),
			Employee.sd_salary_batch.as_("salary_batch"),
			Employee.name.as_("employee"),
			Employee.employee_name,
			Employee.sd_default_salary_slip_method,
			Employee.nick_name,
			Employee.sd_shift_rate.as_("shift_rate"),
			Employee.status,
			Employee.department,
			Employee.employment_type,
			Employee.designation,
			Employee.branch,
			Employee.salary_mode,
		)
	)

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
	# q = q.orderby(Employee.sd_attendance_book_serial.isnull())
	# q = q.orderby(Employee.sd_attendance_book_serial)
	q = q.orderby(Employee.sd_salary_batch)
	q = q.orderby(Employee.name)

	data = q.run(as_dict=True)
	return data

def get_previous_canteen_amount(filters):
	q1 = """
	WITH ranked_messages AS (
		SELECT s.employee, s.canteen, ROW_NUMBER() OVER (PARTITION BY s.employee ORDER BY s.creation DESC) AS rn
		FROM `tabSD Salary Slip` AS s, `tabEmployee` AS e
		where s.employee = e.name
	"""
	q2 = """
	)
	SELECT * FROM ranked_messages WHERE rn = 1;
	"""
	values = {}
	if filters:
		if filters.get('from_date'):
			q1 += " and s.date < %(date)s"
			values['date'] = filters.get('from_date')
		if filters.get('employee'):
			q1 += " and e.name = %(employee)s"
			values['employee'] = filters.get('employee')
		if filters.get('department'):
			q1 += " and e.department =  %(department)s"
			values['department'] = filters.get('department')
		if filters.get('employment_type'):
			q1 += " and e.employment_type = %(employment_type)s"
			values['employment_type'] = filters.get('employment_type')
		if filters.get('designation'):
			q1 += " and e.designation = %(designation)s"
			values['designation'] = filters.get('designation')
		if filters.get('branch'):
			q1 += " and e.branch = %(branch)s"
			values['branch'] = filters.get('branch')
		if filters.get('salary_mode'):
			q1 += " and s.salary_mode = %(salary_mode)s"
			values['salary_mode'] = filters.get('salary_mode')
	results = frappe.db.sql(q1+q2, values=values, as_dict=1)
	d = {}
	for r in results:
		if r.employee not in d:
			d[r.employee] = r
	return d

def get_salary_slips(employees=None, filters=None):
	SalarySlip = frappe.qb.DocType("SD Salary Slip")

	q = (
		frappe.qb.from_(SalarySlip)
		.select(
			SalarySlip.name,
			SalarySlip.employee,
			SalarySlip.date,
			SalarySlip.salary_amount,
			SalarySlip.other_additions,
			SalarySlip.canteen,
			SalarySlip.advance,
			SalarySlip.leave,
			SalarySlip.esi_pf,
			SalarySlip.via_cash,
			SalarySlip.other_deductions,
			SalarySlip.total_deductions,
			SalarySlip.total_amount,
			SalarySlip.docstatus
		).where(SalarySlip.docstatus != 2)
	)
	if filters:
		if filters.get('from_date'):
			q = q.where(SalarySlip.date >= filters.get('from_date'))
		if filters.get('to_date'):
			q = q.where(SalarySlip.date <= filters.get('to_date'))
		if filters.get("salary_mode"):
			q = q.where(SalarySlip.salary_mode == filters.get("salary_mode"))	
	if employees:
		q = q.where(SalarySlip.employee.isin(employees))
	
	salary_slips = q.run(as_dict=True)

	ss = {}
	for slip in salary_slips:
		if slip.employee not in ss:
			ss[slip.employee] = []
		ss[slip.employee].append(slip)
	return ss

def get_data(filters=None):
	employees = get_all_active_employees(filters)
	emp_names = [emp.employee for emp in employees]
	salary_slips = get_salary_slips(emp_names, filters)
	previous_canteen = get_previous_canteen_amount(filters)
	multiple_entry = []
	for employee in employees:
		attendance_list = frappe.get_list("Attendance", filters={
				"employee": employee.employee,
				"attendance_date":["between", [filters.from_date,filters.to_date]],
				"docstatus": 1,
				"status":["in",["Present","Work From Home","Half Day"]]
			}
		)
		res = frappe.db.sql(
			f"""
				WITH ranked_entries AS (
					SELECT running_balance, ROW_NUMBER() OVER (PARTITION BY employee,type ORDER BY posting_datetime DESC) AS rn
					FROM `tabEssdee Advance Ledger Entry` where is_cancelled=0 and employee='{employee.employee}'
					and type = 'Advance'
				)
				SELECT running_balance FROM ranked_entries WHERE rn = 1
			""",as_dict=True
		)
		advance_balance = res[0].running_balance if res else 0
		if employee.employee in salary_slips:
			if len(salary_slips[employee.employee]) > 1:
				multiple_entry.append(employee.employee)
			else:
				ss = salary_slips[employee.employee][0]
				employee.update({
					"salary_slip_name": ss.name,
					"date": ss.date,
					"salary_amount": ss.salary_amount,
					"other_additions": ss.other_additions,
					"canteen": ss.canteen,
					"advance": ss.advance,
					"leave": ss.leave,
					"esi_pf": ss.esi_pf,
					"via_cash": ss.via_cash,
					"other_deductions": ss.other_deductions,
					"total_deductions": ss.total_deductions,
					"total_amount": ss.total_amount,
					"docstatus": ss.docstatus,
				})
		employee.update({
			"salary_slip_method":employee.sd_default_salary_slip_method,
			"no_of_days_worked": len(attendance_list),
			"current_advance_balance": advance_balance,
		})		
		if employee.employee in previous_canteen:
			employee.update({
				"previous_canteen": previous_canteen[employee.employee].canteen,
			})
	if len(multiple_entry) > 0:
		frappe.throw(f"The below Employees have multiple Salary Slip in this date range.<br>{'<br>'.join(multiple_entry)}")
	return employees





