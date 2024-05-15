
import frappe

def execute():
    docs = frappe.get_all("SD Salary Slip", filters = {"docstatus":0},pluck="name")
    for docname in docs:
        doc = frappe.get_doc("SD Salary Slip", docname)
        if not doc.posting_time:
            doc.posting_time = "00:00:00"
            doc.method = "Regular"
            doc.save()
            doc.submit()        
