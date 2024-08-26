# Copyright (c) 2024, Aerele and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from erpnext.stock.utils import get_combine_datetime

class EssdeeAdvanceLedgerEntry(Document):
	def validate(self):
		self.posting_datetime = get_combine_datetime(self.posting_date, self.posting_time)
