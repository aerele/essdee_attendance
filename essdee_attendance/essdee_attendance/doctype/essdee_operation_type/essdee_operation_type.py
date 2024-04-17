# Copyright (c) 2024, Aerele and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class EssdeeOperationType(Document):
	def validate(self):
		if not self.rate:
			frappe.throw('Please Enter Valid Rate')