# Copyright (c) 2024, Aerele and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import datetime
from frappe.utils import flt
from essdee_attendance.essdee_attendance.advance_ledger import make_ledger, cancel_ledger
from erpnext.stock.utils import get_combine_datetime


class SDSalarySlip(Document):
	def autoname(self):
		today = datetime.date.today()
		year = str(today.year)[-2:]
		current_week = today.isocalendar().week
		self.naming_series = f'SS-{year}{current_week:02}-'

	def validate(self):
		self.posting_datetime = get_combine_datetime(self.date, self.posting_time)
		self.calculate_total()
		self.validate_employee()
	
	def calculate_total(self):
		self.total_deductions = (get_float(self.advance) + get_float(self.canteen) + get_float(self.esi_pf) + get_float(self.other_deductions) + get_float(self.leave) + get_float(self.via_cash))
		total =self.salary_amount + (get_float(self.other_additions)) - (get_float(self.total_deductions))
		if self.method == 'Pay Later':
			self.pay_later_amount = total
			self.total_amount = 0
		else:
			self.pay_later_amount = 0
			self.total_amount = total
	
	def validate_employee(self):
		if frappe.flags.in_patch:
			return
		status = frappe.get_value("Employee", self.employee, "status")
		if status != 'Active':
			frappe.throw("Salary Slip can be created only for active employees.")

	def on_submit(self):
		if frappe.flags.in_patch or frappe.flags.in_migrate:
			return
		details = get_ledger_entry(self)
		make_ledger(details)
	
	def on_cancel(self):
		cancel_ledger(self.name,'SD Salary Slip')

def get_float(x):
	if not x:
		return 0
	return x

def get_ledger_entry(doc):
	x = []
	if doc.method == 'Pay Later':
		dic = {
			"employee" : doc.employee,
			"posting_date" : doc.date,
			"posting_time" : doc.posting_time,
			"posting_datetime": doc.posting_datetime,
			"amount": doc.pay_later_amount,
			"type":"Pay Later",
			"doctype" : "SD Salary Slip",
			"docname" : doc.name
		}
		x.append(dic)	

	if doc.advance:
		dic = {
			"employee" : doc.employee,
			"posting_date" : doc.date,
			"posting_time" : doc.posting_time,
			"posting_datetime": doc.posting_datetime,
			"amount": flt(doc.advance) * flt(-1) ,
			"type":"Advance",
			"doctype" : "SD Salary Slip",
			"docname" : doc.name
		}
		x.append(dic)

	return x