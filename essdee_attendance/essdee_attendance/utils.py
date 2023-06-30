import frappe

@frappe.whitelist()
def trial_expired():
    return False
