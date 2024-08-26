import frappe
from essdee_attendance.essdee_attendance.advance_ledger import make_ledger
from essdee_attendance.essdee_attendance.doctype.sd_salary_slip.sd_salary_slip import get_ledger_entry

def execute():
    docs = frappe.get_all("SD Salary Slip", pluck="name", filters={
        "method": "Pay Later",
        "docstatus": 1,
        "total_amount": 0,
        "pay_later_amount": ["!=", 0],
    })

    for docname in docs:
        doc = frappe.get_doc("SD Salary Slip", docname)
        entry = get_ledger_entry(doc)
        make_ledger(entry)