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
	columns = [
		{'fieldname': 'employee', 'fieldtype': 'Data', 'label': 'Employee','width':170},
		{'fieldname': 'type', 'fieldtype': 'Data', 'label': 'Type','width':170},
		{'fieldname': 'running_balance', 'fieldtype': 'Currency', 'label': 'Balance','width':170},
	]
	return columns

def get_data(filters):
    Ledger_Entry = frappe.qb.DocType('Essdee Advance Ledger Entry')
    query = frappe.qb.from_(Ledger_Entry).select(
        Ledger_Entry.employee,
        Ledger_Entry.type,
        Ledger_Entry.running_balance
    ).where(
        Ledger_Entry.is_cancelled == False
    )

    if filters.get('employee'):
        query = query.where(Ledger_Entry.employee == filters.get('employee'))
    if filters.get('type'):
        query = query.where(Ledger_Entry.type == filters.get('type'))
    if filters.get('to_date'):
        query = query.where(Ledger_Entry.posting_date <= filters.get('to_date'))

    query = query.orderby(Ledger_Entry.posting_date, order=Order.desc).limit(1)
    result = query.run(as_dict=True)
    return result
