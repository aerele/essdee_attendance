import frappe,json
from frappe.utils import flt
from datetime import datetime

@frappe.whitelist()
def trial_expired():
    return False

