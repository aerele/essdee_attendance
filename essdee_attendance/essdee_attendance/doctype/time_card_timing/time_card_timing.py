# Copyright (c) 2024, Aerele and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class TimeCardTiming(Document):
	def autoname(self):
		date = str(self.date)
		year, month, date = date.split("-")
		self.name = str(self.employee)+"-"+date+"-"+month+"-"+year
