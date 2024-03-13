import frappe

def validate(doc, action):
    if action != "validate": return
    if doc.is_new():
        doc.sd_bank_account_status = ''
        return
    old_doc = frappe.get_doc("Employee", doc.name)
    if (old_doc.bank_ac_no != doc.bank_ac_no) or (old_doc.ifsc_code != doc.ifsc_code):
        doc.sd_bank_account_status = 'Pending Approval'