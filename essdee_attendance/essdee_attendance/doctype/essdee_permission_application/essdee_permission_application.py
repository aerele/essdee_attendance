# Copyright (c) 2024, Aerele and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import get_datetime, time_diff_in_hours, get_timedelta
from erpnext.stock.utils import get_combine_datetime
from datetime import datetime , timedelta
from frappe.utils import cint

import frappe.utils
from frappe import bold

class EssdeePermissionApplication(Document):	
	def after_insert(self):
		self.notify_approver_pwa()

	def notify_approver_pwa(self):
		from_user = frappe.db.get_value("Employee", self.employee, "user_id", cache=True)
		to_user = self.get('permission_approver')

		if not to_user or from_user == to_user:
			return

		notification = frappe.new_doc("PWA Notification")
		notification.message = (
			f"{bold(self.employee_name)} raised a new {bold(self.doctype)} for approval: {self.name}"
		)
		notification.from_user = from_user
		notification.to_user = to_user

		notification.reference_document_type = self.doctype
		notification.reference_document_name = self.name
		notification.insert(ignore_permissions=True)

	
	def before_save(self):
		roles = frappe.get_roles()
		if 'Employee' in roles and self.permission_approver:	
			doc = frappe.get_single('Essdee Attendance Settings')
			args = self.as_dict()
			try:
				email_template = frappe.get_doc("Email Template",doc.permission_email_template)
				message = frappe.render_template(email_template.response_, args)
				self.notify(
					{
						"message": message,
						"message_to": self.permission_approver,
						"subject": email_template.subject,
					}
				)
			except:
				pass	
			

	def notify(self, args):
		args = frappe._dict(args)
		contact = args.message_to
		if not isinstance(contact, list):
			contact = frappe.get_doc("User", contact).email or contact
		try:
			frappe.sendmail(
				recipients=contact,
				subject=args.subject,
				message=args.message,
				)
			frappe.msgprint("Email sent")
		except frappe.OutgoingEmailError:
			pass
	
	def before_submit(self):
		if self.status == 'Open':
			frappe.throw("The permission is in open status")
		
		if not "Leave Approver" in frappe.get_roles():
			frappe.throw("You are not permitted to submit the document")
		

	def before_validate(self):
		employee_details = get_employee_details(self.employee)
		self.employee_name = employee_details['employee_name']
		shift_type = frappe.get_value("Employee", {'name': self.employee}, 'default_shift')
		starts,ends = frappe.get_value("Shift Type", {'name': shift_type}, ['start_time','end_time'])
		doc = frappe.get_single("Essdee Attendance Settings")
		if get_timedelta(self.start_time) > ends :
			frappe.throw(f"Start time is greater than {self.employee}'s shift end time"),
		if get_timedelta(self.start_time) < starts:
			self.start_time = starts
		if self.permission_type == "Personal Permission":
			if get_timedelta(self.start_time) < get_timedelta("13:00:00"):
				frappe.throw("Permission is not applicable for Morning Shift")
			self.end_date = self.start_date

			self.end_time = calculate_end_time(ends, self.start_time,doc.personal_permission_hours)
			
			perm_list = check_permission_limit(self.posting_date, self.name, self.employee, doc.personal_permission_limit, self.employee_name)
			
			check_permission_on_same_day(perm_list, self.start_date, self.name)

		if self.end_time:
			if get_timedelta(self.end_time) > ends:
				self.end_time = ends

		self.start_datetime = get_combine_datetime(self.start_date,self.start_time)
		self.end_datetime = get_combine_datetime(self.end_date, self.end_time)

		if self.start_datetime > self.end_datetime:
			frappe.throw("End time and date is higher than start time and date")
		
		check_available(self.start_datetime, self.end_datetime, self.employee, self.name)
		
		if self.status != 'Open' and not "Leave Approver" in frappe.get_roles():
			frappe.throw("You are not permitted to Approve or Reject the Permission")

def check_permission_limit(posting_date, doc_name, employee, personal_permission_limit, employee_name):
	perm_doc = frappe.qb.DocType('Essdee Permission Application')
			
	query = (
		frappe.qb.from_(perm_doc)
		.select('name')
		.where(
			(perm_doc.posting_date.between(datetime.today().replace(day=1),posting_date)) &
			(perm_doc.employee == employee) &
			(perm_doc.status == 'Approved') &
			(perm_doc.name != doc_name) &
			(perm_doc.permission_type == 'Personal Permission')
		)
	)

	perm_list = query.run()
	if len(perm_list) >= personal_permission_limit:
		frappe.throw(f"{employee_name}'s permission limit is reached it's limit")
	
	return perm_list

def check_permission_on_same_day(perm_list, start_date, self_name):
	for perm in perm_list:
		doc = frappe.get_doc("Essdee Permission Application",perm)
		if str(doc.start_date) == str(start_date) and doc.name != self_name:
			frappe.throw("Only one permission is applicable for a day")	

def calculate_end_time(ends, start_time, personal_permission_hours):
	time_diff = time_diff_in_hours(str(ends), str(start_time))
	end_time = None
	if time_diff <= personal_permission_hours:
		end_time = ends
	else:
		end_time = get_timedelta(start_time) + timedelta(hours=personal_permission_hours)	
	return end_time

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
	name,leave_approver,department = frappe.get_value('Employee',employee,['employee_name','leave_approver','department'])

	if not leave_approver and department:
		leave_approver = frappe.db.get_value("Department Approver",
			{"parent": department, "parentfield": "leave_approvers", "idx": 1},"approver")

	return {
		'employee_name': name,
		'leave_approver':leave_approver
	}

# @frappe.whitelist()
# def valid_start_and_end_datetime(start_time,employee,type):
# 	shift_type = frappe.get_value("Employee", {'name': employee}, 'default_shift')
# 	starts,end_time = frappe.get_value("Shift Type", {'name': shift_type}, ['start_time','end_time'])
# 	if get_timedelta(start_time) > end_time :
# 		return {
# 			'start' : starts,
# 			'end' : None,
# 			'msg': f"Start time is greater than {employee}'s shift end time",
# 		}
# 	if get_timedelta(start_time) < starts:
# 		return {
# 			'start': starts,
# 			'end': None,
# 			'msg':f"Start time is less than {employee}'s shift start time",
# 		}		
# 	doc = frappe.get_single("Essdee Attendance Settings")
# 	end = None
	
# 	if type == "Personal Permission":
# 		time_diff = time_diff_in_hours(str(end_time), start_time)
# 		if time_diff <= doc.personal_permission_hours:
# 			end= end_time
# 		else:
# 			end = get_timedelta(start_time) + timedelta(hours=doc.personal_permission_hours)
# 	return {
# 		'start': None,
# 		'end': end,
# 		'msg':None,
# 	}	

# @frappe.whitelist()
# def valid_endtime(end_time,employee):
# 	shift_type = frappe.get_value("Employee", {'name': employee}, 'default_shift')
# 	start, end = frappe.get_value("Shift Type", {'name': shift_type}, ['start_time','end_time'])
# 	if end < get_timedelta(end_time):
# 		return {
# 			'end': end,
# 			'msg': f"End time is greater than {employee}'s shift end time",
# 		}
# 	if start > get_timedelta(end_time):
# 		return {
# 			'end':end,
# 			'msg': f"End time is less than {employee}'s shift start time",
# 		}
# 	return {
# 		'end': None,
# 		'msg': None,
# 	}

@frappe.whitelist()
def submit_doc(doc_name, status):
	if not "Leave Approver" in frappe.get_roles():
		frappe.throw("You are not permitted to submit the document")
		
	doc = frappe.get_doc("Essdee Permission Application", doc_name)
	doc.status = status
	doc.submit()

@frappe.whitelist()
def send_email(doc_name):
	doc = frappe.get_doc('Essdee Permission Application', doc_name)
	doc.before_save()