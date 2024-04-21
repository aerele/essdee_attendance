# Copyright (c) 2024, Aerele and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import datetime


class SDSalarySlip(Document):
	def autoname(self):
		today = datetime.date.today()
		year = str(today.year)[-2:]
		current_week = today.isocalendar().week
		self.naming_series = f'SS-{year}{current_week:02}-'

	def validate(self):
		self.calculate_total()
		self.validate_employee()
	
	def calculate_total(self):
		self.total_deductions = (get_float(self.advance) + get_float(self.canteen) + get_float(self.esi_pf) + get_float(self.other_deductions) + get_float(self.leave) + get_float(self.via_cash))
		self.total_amount = self.salary_amount + (get_float(self.other_additions)) - (get_float(self.total_deductions))
	
	def validate_employee(self):
		status = frappe.get_value("Employee", self.employee, "status")
		if status != 'Active':
			frappe.throw("Salary Slip can be created only for active employees.")

def get_float(x):
	if not x:
		return 0
	return x