import frappe,json
from frappe.model.document import Document
import datetime


class EssdeeWorkEntry(Document):
	def validate(self):
		for d in self.details:
			d.total = d.quantity* d.rate
			
@frappe.whitelist()
def get_employee_operations(employee):
	doc = frappe.get_doc('Employee',employee)
	table_data = doc.essdee_employee_operations
	print(table_data)
	operation_rates = []
	for data in table_data:
		rate = data.rate
		if not rate:
			operation_type = frappe.get_doc('Essdee Operation Type',data.operation)
			rate = operation_type.rate
		operation_rates.append({'operation': data.operation, 'rate': rate})
	return operation_rates	

@frappe.whitelist()
def get_operation_rate(employee, operation):
	rate = None
	if employee:
		doc = frappe.get_doc("Employee",employee)
		operation_table = doc.essdee_employee_operations
		for data in operation_table:
			if data.operation == operation:
				rate = data.rate
				break
	if not rate:
		doc = frappe.get_doc('Essdee Operation Type',operation)
		rate = doc.rate
	return rate
