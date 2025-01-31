# Copyright (c) 2024, Aerele and contributors
# For license information, please see license.txt

import frappe
from frappe.query_builder import Order

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_columns():
	columns =[
		{
			'fieldname': 'employee',
			'fieldtype': 'Link',
			'label': 'Employee',
			"options": "Employee",
			'width':170
		},
		{
			'fieldname':'type',
			'fieldtype': 'Data',
			'label': 'Type',
			'width':120
		},
		{
			'fieldname':'amount',
			'fieldtype': 'Currency',
			'label': 'Amount',
			'width':120
		},
		{
			'fieldname':'running_balance',
			'fieldtype': 'Currency',
			'label': 'Balance',
			'width':120
		},
		{
			'fieldname':'posting_date',
			'fieldtype': 'Date',
			'label': 'Posting Date',
			'width':120
		},
		{
			'fieldname':'posting_time',
			'fieldtype': 'Time',
			'label': 'Posting Time',
			'width':120
		},
		{
			'fieldname':'transaction_type',
			'fieldtype': 'Data',
			'label': 'Transaction Type',
			'width':200
		},
		{
			'fieldname':'transaction_name',
			'fieldtype': 'Dynamic Link',
			'label': 'Transaction Name',
			"options": "transaction_type",
			'width':150
		},
	]
	return columns

def get_data(filters):
	Ledger_Entry = frappe.qb.DocType('Essdee Advance Ledger Entry')
	Employee = frappe.qb.DocType('Employee')

	query = (
		frappe.qb.from_(Ledger_Entry).from_(Employee)
		.select(
			Ledger_Entry.employee,
			Ledger_Entry.type,
			Ledger_Entry.amount,
			Ledger_Entry.running_balance,
			Ledger_Entry.posting_date,
			Ledger_Entry.posting_time,
			Ledger_Entry.transaction_type,
			Ledger_Entry.transaction_name,
		)
		.where(Ledger_Entry.employee == Employee.name)
		.where(Ledger_Entry.is_cancelled == False)
	)

	# query = frappe.qb.from_(Ledger_Entry).select('*').where(Ledger_Entry.is_cancelled == False)
	if filters.employee:
		query = query.where(Employee.name == filters.employee)
	if filters.department:
		query = query.where(Employee.department == filters.department)
	if filters.type:
		query = query.where(Ledger_Entry.type == filters.type)
	if filters.from_date and filters.to_date:
		query = query.where(Ledger_Entry.posting_date.between(filters.from_date, filters.to_date))

	query = query.orderby(Ledger_Entry.posting_datetime, order=Order.desc)	
	result = query.run(as_dict = True)	
	return result
