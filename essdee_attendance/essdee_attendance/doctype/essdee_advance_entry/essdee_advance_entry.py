# Copyright (c) 2024, Aerele and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from essdee_attendance.essdee_attendance.advance_ledger import make_ledger
from essdee_attendance.essdee_attendance.advance_ledger import cancel_ledger
from erpnext.stock.utils import get_combine_datetime

class EssdeeAdvanceEntry(Document):
	def validate(self):
		self.posting_datetime = get_combine_datetime(self.posting_date, self.posting_time)
	
	def on_submit(self):
		details = get_list(self)
		make_ledger(details)
	def on_cancel(self):
		cancel_ledger(self.name,'Essdee Advance Entry')	


def get_list(doc):
	x = []
	for row in doc.essdee_advance_entry_details:
		dic = {
			"employee" : row.employee,
			"posting_date" : doc.posting_date,
			"posting_time" : doc.posting_time,
			"posting_datetime": doc.posting_datetime,
			"amount": row.amount,
			"type":row.type,
			"doctype" : "Essdee Advance Entry",
			"docname" : doc.name
		}
		x.append(dic)		
	return x	