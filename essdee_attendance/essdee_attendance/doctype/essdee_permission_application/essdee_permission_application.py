# Copyright (c) 2024, Aerele and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import get_datetime
from erpnext.stock.utils import get_combine_datetime
from datetime import datetime 

class EssdeePermissionApplication(Document):
	def before_validate(self):
		self.start_datetime = get_combine_datetime(self.start_date,self.start_time)
		self.end_datetime = get_combine_datetime(self.end_date, self.end_time)

		if self.start_datetime > self.end_datetime:
			frappe.throw("End time and date is higher than start time and date")
		
		if self.permission_type == 'Personal Permission':
			perm_list = frappe.get_list('Essdee Permission Application', {
				'employee': self.employee, 
				'permission_type': self.permission_type, 
				'posting_date': ['between',datetime.today().replace(day=1), self.posting_date]
				},
				pluck = 'name')
			
			doc = frappe.get_single('Essdee Attendance Settings')

			if len(perm_list) == doc.permission_hours:
				frappe.throw(f"You have already {doc.permission_hours} permissions for this month")
			
			for perm in perm_list:
				doc = frappe.get_doc("Essdee Permission Application",perm)
				if str(doc.start_date) == str(self.start_date) and doc.name != self.name:
					frappe.throw("Only one permission is applicable for a day")	

			check_available(self.start_datetime, self.end_datetime, self.employee, self.name)
		else:
			check_available(self.start_datetime, self.end_datetime, self.employee, self.name)

def check_available(start_datetime, end_datetime, employee, doc_name):
	start_datetime = get_datetime(start_datetime)
	end_datetime = get_datetime(end_datetime)
	doctype = frappe.qb.DocType("Essdee Permission Application")
	query = (
		frappe.qb.from_(doctype)
		.select('*')
		.where(
			(doctype.employee == employee) &
			(doctype.name != doc_name) &
			(
				((doctype.start_datetime > start_datetime) & (doctype.end_datetime < end_datetime)) |
				((doctype.start_datetime > end_datetime) & (doctype.end_datetime < end_datetime)) |
				(doctype.start_datetime.between(start_datetime, end_datetime)) |
				(doctype.end_datetime.between(start_datetime, end_datetime)) |
				((start_datetime > doctype.start_datetime) & (start_datetime < doctype.end_datetime))|
				((end_datetime  < doctype.end_datetime) & (end_datetime > doctype.start_datetime))
			)
		)
	)
	res = query.run(as_dict=True)
	if len(res) > 0:
		frappe.throw("Already you had a permission on that period of time")


@frappe.whitelist()
def get_dept_and_designation(employee):
	dept,design,name = frappe.get_value('Employee',employee,['department','designation','employee_name'])
	return {
		'department' : dept,
		'designation': design,
		'full_name': name
	}

@frappe.whitelist()
def get_site():
	return frappe.utils.get_url()

# time_diff = time_diff_in_hours(self.end_time, self.start_time)
# doc = frappe.get_doc("EssdeePermissionApplication Type", self.essdee_permission_application_type)
# if time_diff > doc.max_hours:
# 	frappe.throw(f"For {self.essdee_permission_application_type} only {doc.max_hours} hours is Applicable")
# decimal = time_diff - int(time_diff)
# point = (60/100)* decimal
# if round(point,2) == 0.6:
# 	point = 1
# self.essdee_permission_application_hours = int(time_diff) + point
