# Copyright (c) 2024, Aerele and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_columns():
	columns =[
		{'fieldname': 'employee', 'fieldtype': 'Data', 'label': 'Employee','width':170},
		{'fieldname': 'type', 'fieldtype': 'Data', 'label': 'Type','width':120},
		{'fieldname': 'amount', 'fieldtype': 'Currency', 'label': 'Amount','width':120},
		{'fieldname': 'running_balance', 'fieldtype': 'Currency', 'label': 'Balance','width':120},
		{'fieldname': 'posting_date', 'fieldtype': 'Date', 'label': 'Posting Date','width':120},
		{'fieldname': 'posting_time', 'fieldtype': 'Time', 'label': 'Posting Time','width':120},
		{'fieldname': 'transaction_type', 'fieldtype': 'Data', 'label': 'Transaction Type','width':200},
		{'fieldname': 'transaction_name', 'fieldtype': 'Data', 'label': 'Transaction Name','width':150},
	]
	return columns

def get_data(filters):
	Ledger_Entry = frappe.qb.DocType('Essdee Advance Ledger Entry')
	query = frappe.qb.from_(Ledger_Entry).select('*').where(Ledger_Entry.is_cancelled == False)
	if filters.employee:
		query = query.where(Ledger_Entry.employee == filters.employee)
	if filters.type:
		query = query.where(Ledger_Entry.type == filters.type)
	if filters.from_date and filters.to_date:
		query = query.where(Ledger_Entry.posting_date.between(filters.from_date, filters.to_date))

	query = query.orderby(Ledger_Entry.posting_datetime)			 
	result = query.run(as_dict = True)	
	return result
