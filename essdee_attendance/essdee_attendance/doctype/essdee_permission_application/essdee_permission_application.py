# Copyright (c) 2024, Aerele and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import get_datetime, time_diff_in_hours, get_timedelta
from erpnext.stock.utils import get_combine_datetime
from datetime import datetime 
from frappe.utils import cint

class EssdeePermissionApplication(Document):	
	def before_save(self):
		roles = frappe.get_roles()
		if 'Employee' in roles:	
			args = self.as_dict()
			email_template = frappe.get_doc("Email Template", "Permission Template")
			message = frappe.render_template(email_template.response_, args)
			self.notify(
				{
					"message": message,
					"message_to": self.permission_approver,
					"subject": email_template.subject,
				}
			)

	def notify(self, args):
		args = frappe._dict(args)
		contact = args.message_to
		if not isinstance(contact, list):
			contact = frappe.get_doc("User", contact).email or contact

		user = frappe.get_doc("User", frappe.session.user)

		try:
			frappe.sendmail(
				recipients=contact,
				sender=user.email,
				subject=args.subject,
				message=args.message,
				)
			frappe.msgprint("Email sent")
		except frappe.OutgoingEmailError:
			pass
	
	def before_submit(self):
		if self.status == 'Open':
			frappe.throw("The permission is in open status")

		if self.permission_approver != frappe.session.user:
			frappe.throw("You are not permitted to submit this document")	

	def before_validate(self):
		self.start_datetime = get_combine_datetime(self.start_date,self.start_time)
		self.end_datetime = get_combine_datetime(self.end_date, self.end_time)

		if self.start_datetime > self.end_datetime:
			frappe.throw("End time and date is higher than start time and date")

		attendance_doc = frappe.get_single('Essdee Attendance Settings')

		if self.permission_type == "Personal Permission":
			perm_list = frappe.get_list('Essdee Permission Application', {
				'employee': self.employee, 
				'permission_type': self.permission_type, 
				'posting_date': ['between',datetime.today().replace(day=1), self.posting_date],
				'status':'Approved',
				'name':['!=',self.name]
				},
				pluck = 'name')

			if len(perm_list) == attendance_doc.personal_permission_limit:
				frappe.throw(f"{self.full_name}'s permission limit is reached it's limit")
			
			for perm in perm_list:
				doc = frappe.get_doc("Essdee Permission Application",perm)
				if str(doc.start_date) == str(self.start_date) and doc.name != self.name:
					frappe.throw("Only one permission is applicable for a day")	

			check_available(self.start_datetime, self.end_datetime, self.employee, self.name)
		else:
			check_available(self.start_datetime, self.end_datetime, self.employee, self.name)
	
def check_available(start_datetime, end_datetime, employee, doc_name):
	from pypika import Order

	start_datetime = get_datetime(start_datetime)
	end_datetime = get_datetime(end_datetime)
	doctype = frappe.qb.DocType("Essdee Permission Application")
	query = (
		frappe.qb.from_(doctype)
		.select('*')
		.where(
			(doctype.employee == employee) &
			(doctype.name != doc_name) &
			(doctype.status == 'Approved') &
			(
				((doctype.start_datetime > start_datetime) & (doctype.end_datetime < end_datetime)) |
				((doctype.start_datetime > end_datetime) & (doctype.end_datetime < end_datetime)) |
				(doctype.start_datetime.between(start_datetime, end_datetime)) |
				(doctype.end_datetime.between(start_datetime, end_datetime)) |
				((start_datetime > doctype.start_datetime) & (start_datetime < doctype.end_datetime)) |
				((end_datetime < doctype.end_datetime) & (end_datetime > doctype.start_datetime))
			)
		)
		.orderby(doctype.start_datetime, order=Order.asc)
		.limit(1)
	)

	res = query.run(as_dict=True)
	if res:
		frappe.throw(f"Already you had a permission From {res[0]['start_datetime']} To {res[0]['end_datetime']}")

@frappe.whitelist()
def get_employee_details(employee):
	dept,design,name,leave_approver,department = frappe.get_value('Employee',employee,['department','designation','employee_name','leave_approver','department'])

	if not leave_approver and department:
		leave_approver = frappe.db.get_value("Department Approver",
			{"parent": department, "parentfield": "leave_approvers", "idx": 1},"approver")

	return {
		'department' : dept,
		'designation': design,
		'full_name': name,
		'leave_approver':leave_approver
	}

@frappe.whitelist()
def valid_start_and_end_datetime(start_time,employee,type):
	shift_type = frappe.get_value("Employee", {'name': employee}, 'default_shift')
	starts,end_time = frappe.get_value("Shift Type", {'name': shift_type}, ['start_time','end_time'])
	if get_timedelta(start_time) > end_time :
		return {
			'start' : starts,
			'end' : None,
			'msg': f"Start time is greater than {employee}'s shift end time",
		}
	if get_timedelta(start_time) < starts:
		return {
			'start': starts,
			'end': None,
			'msg':f"Start time is less than {employee}'s shift start time",
		}		
	doc = frappe.get_single("Essdee Attendance Settings")
	end = None
	
	if type == "Personal Permission":
		time_diff = time_diff_in_hours(str(end_time), start_time)
		if time_diff <= doc.personal_permission_hours:
			end= end_time
		else:
			arr = start_time.split(":")
			arr[0] = str(int(arr[0]) + doc.personal_permission_hours)
			end= ":".join(arr)
	return {
		'start': None,
		'end': end,
		'msg':None,
	}	

@frappe.whitelist()
def valid_endtime(end_time,employee):
	shift_type = frappe.get_value("Employee", {'name': employee}, 'default_shift')
	start, end = frappe.get_value("Shift Type", {'name': shift_type}, ['start_time','end_time'])
	if end < get_timedelta(end_time):
		return {
			'end': end,
			'msg': f"End time is greater than {employee}'s shift end time",
		}
	if start > get_timedelta(end_time):
		return {
			'end':end,
			'msg': f"End time is less than {employee}'s shift start time",
		}
	return {
		'end': None,
		'msg': None,
	}

@frappe.whitelist()
def submit_doc(doc_name):
	doc = frappe.get_doc("Essdee Permission Application", doc_name)
	doc.submit()