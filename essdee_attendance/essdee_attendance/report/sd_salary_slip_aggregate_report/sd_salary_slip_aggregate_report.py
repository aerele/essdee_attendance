# Copyright (c) 2025, Aerele and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    columns, data = get_columns(), get_data(filters)
    return columns, data

def get_columns():
    columns = [
        {"fieldname": "employee", "fieldtype": "Link", "label": "Employee", "options": "Employee"},
        {"fieldname": "employee_name", "fieldtype": "Data", "label": "Employee Name"},
        {"fieldname": "salary_amount", "fieldtype": "Currency", "label": "Salary Amount"},
        {"fieldname": "other_additions", "fieldtype": "Currency", "label": "Other Additions"},
        {"fieldname": "canteen", "fieldtype": "Currency", "label": "Canteen"},
        {"fieldname": "leave_deductions", "fieldtype": "Currency", "label": "Leave"},
        {"fieldname": "other_deductions", "fieldtype": "Currency", "label": "Other Deductions"},
        {"fieldname": "via_cash", "fieldtype": "Currency", "label": "Via Cash"},
        {"fieldname": "advance", "fieldtype": "Currency", "label": "Advance"},
        {"fieldname": "esi_pf", "fieldtype": "Currency", "label": "ESI/PF"},
        {"fieldname": "total_deductions", "fieldtype": "Currency", "label": "Total Deductions"},
        {"fieldname": "pay_later_amount", "fieldtype": "Currency", "label": "Pay Later Amount"},
        {"fieldname": "total_amount", "fieldtype": "Currency", "label": "Total Amount"},
        {"fieldname": "method", "fieldtype": "Data", "label": "Method"},
    ]
    return columns

def get_data(filters=None):
    additional = ""
    if filters and filters.get("salary_slip_method"):
        additional += f" AND method = '{filters.get('salary_slip_method')}'"
    result = frappe.db.sql(
        f"""
            SELECT employee, employee_name, SUM(salary_amount) AS salary_amount, SUM(other_additions) AS other_additions,
            SUM(canteen) AS canteen, SUM(`leave`) AS leave_deductions, SUM(other_deductions) AS other_deductions, SUM(via_cash) AS via_cash,
            SUM(advance) AS advance, SUM(esi_pf) AS esi_pf, SUM(total_deductions) AS total_deductions, SUM(pay_later_amount) AS pay_later_amount,
            SUM(total_amount) AS total_amount, method
            FROM `tabSD Salary Slip` 
            WHERE date BETWEEN '{filters.get('from_date')}' AND '{filters.get('to_date')}' AND docstatus = 1 {additional}
            GROUP BY employee, method
        """,
        as_dict=True
    )
    return result
