import frappe,json
from frappe.model.document import Document
import datetime


class EssdeeWorkEntry(Document):
	def validate(self):
		for d in self.details:
			d.total = d.quantity* d.rate
			
@frappe.whitelist()
def get_employee_operations(employee):
	employee_operations = frappe.get_all("Essdee Employee Operation", fields=['operation', 'rate'], filters={'parent': employee})
	operation_rates = []
	for data in employee_operations:
		rate = data.rate
		if not rate:
			rate = frappe.get_value('Essdee Operation Type', data.operation, 'rate')
		operation_rates.append({'operation': data.operation, 'rate': rate})
	return operation_rates	

@frappe.whitelist()
def get_operation_rate(employee, operation):
	rate = None
	if employee:
		employee_operations = frappe.get_all("Essdee Employee Operation", fields=['operation', 'rate'], filters={'parent': employee})
		for data in employee_operations:
			if data.operation == operation:
				rate = data.rate
				break
	if not rate:
		rate = frappe.get_value('Essdee Operation Type',operation,'rate')
	return rate
