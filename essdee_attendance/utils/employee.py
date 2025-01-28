import frappe
from frappe.utils import getdate

def validate(doc, action):
    if action != "validate": return
    if doc.is_new():
        doc.sd_bank_account_status = ''
        return
    old_doc = frappe.get_doc("Employee", doc.name)
    if (old_doc.bank_ac_no != doc.bank_ac_no) or (old_doc.ifsc_code != doc.ifsc_code):
        doc.sd_bank_account_status = 'Pending Approval'

@frappe.whitelist()
def get_date(from_date):
	from_date = getdate(from_date)
	date = from_date.day
	month = from_date.month
	year = from_date.year 
	return str(date)+"/"+str(month)+"/"+str(year)