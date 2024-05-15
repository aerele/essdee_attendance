# Copyright (c) 2024, Aerele and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_columns():
	columns = [
		{'fieldname': 'employee', 'fieldtype': 'Link', 'label': 'Employee',"options":"Employee",'width':170},
		{'fieldname': 'type', 'fieldtype': 'Data', 'label': 'Type','width':170},
		{'fieldname': 'running_balance', 'fieldtype': 'Currency', 'label': 'Balance','width':170},
	]
	return columns

def get_data(filters):
    conditions = ""
    con = {}
    if filters.get('employee'):
        conditions += f" and employee = %(employee)s"
        con["employee"] = filters.get("employee")
    if filters.get('type'):
        conditions += f" and type = %(type)s"
        con["type"] = filters.get("type")
    if filters.get('to_date'):
        conditions += f" and posting_date <= %(date)s"
        con["date"] = filters.get("to_date")    
    
    query = f"""
        WITH ranked_entries AS (
            SELECT 
                *,
                ROW_NUMBER() OVER (PARTITION BY employee,type ORDER BY posting_datetime DESC) AS rn
            FROM `tabEssdee Advance Ledger Entry` where 1=1 {conditions}
        )
        SELECT * FROM ranked_entries WHERE rn = 1;
        """
    print(query)
    doc = frappe.db.sql(query,
        con,
        as_dict=True
    )
    return doc