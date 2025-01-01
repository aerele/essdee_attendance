import frappe
from hrms.api import get_workflow, get_workflow_state_field, get_allowed_states_for_workflow, get_department_approvers

import frappe,json

@frappe.whitelist()
def get_employees(**args):
    fields = ['name', 'employee', 'first_name', 'employee_name'] 
    employees = frappe.get_list('Employee', fields=fields)
    return employees

@frappe.whitelist()
def get_selected_employees(**args):
    employees = args.get('employees')
    employees = json.loads(employees)
    fields = [
		'name', 'first_name', 'last_name', 'gender', 'date_of_birth', 'status', 'company', 'department', 'designation',
		'person_to_be_contacted', 'blood_group', 'emergency_phone_number', 'image', 'sd_signature_upload',
		'father_or_spouse', 'relation_', 'sd_nature_of_employee', 'branch', 'date_of_joining', 'current_address', 'permanent_address'
	] 
    temp = frappe.get_list('Employee',filters={'name': ['in', employees]}, fields=fields)
    return temp

@frappe.whitelist()
def get_employees_by_filters(**args):
    filters = args["filters"]
    fields = ['name', 'employee', 'first_name', 'employee_name'] 
    employees = frappe.get_list('Employee',filters=filters, fields=fields)
    return employees

@frappe.whitelist()
def store_employees(**args):
    employees = args['Employees']
    employees = json.loads(employees)
    doc = frappe.get_single('Employee ID Card')
    doc.child_table=[]
    for employee in employees:
        branch = frappe.get_doc("Branch", employee['branch'])
        doc.append('child_table',{
            'employee_id':employee['name'],
            'first_name':employee['first_name'],
            'gender':employee['gender'],
            'date_of_birth':employee['date_of_birth'],
			'designation':employee['designation'],
            'status':employee['status'],
            'company':employee['company'],
            'department':employee['department'],
            'person_to_be_contacted':employee['person_to_be_contacted'],
            'father_or_spouse':employee['father_or_spouse'],
            'blood_group':employee['blood_group'],
            'emergency_phone_number':employee['emergency_phone_number'],
            'image':employee['image'],
            'sd_signature_upload':employee['sd_signature_upload'],
            'relation': employee['relation_'],
			'employee_nature':employee['sd_nature_of_employee'],
			'branch':employee['branch'],
			'date_of_joining':employee['date_of_joining'],
			'current_address':employee['current_address'],
			'permanent_address':employee['permanent_address'],
			'branch_title': branch.branch_address_title,
			'branch_address': branch.branch_address,
        })
    doc.save(ignore_permissions=True) 
    return True

# HRMS PWA functions

@frappe.whitelist()
def get_permission_applications(employee: str,
	approver_id: str | None = None,
	for_approval: bool = False,
	limit: int | None = None,
) -> list[dict]:
	filters = get_permission_application_filters(employee, approver_id, for_approval)
	fields = [
		"name",
		"posting_date",
		"employee",
		"full_name",
		"permission_type",
		"status",
		"start_date",
		"end_date",
		"start_time",
		"end_time",
		"purpose",
	]
	if workflow_state_field := get_workflow_state_field("Essdee Permission Application"):
		fields.append(workflow_state_field)
	

	applications = frappe.get_list(
		"Essdee Permission Application",
		fields=fields,
		filters=filters,
		order_by="start_date desc",
		limit=limit,
	)

	if workflow_state_field:
		for application in applications:
			application["workflow_state_field"] = workflow_state_field

	return applications

def get_permission_application_filters(
	employee: str,
	approver_id: str | None = None,
	for_approval: bool = False,
) -> dict:
	filters = frappe._dict()
	if for_approval:
		filters.docstatus = 0
		filters.employee = ("!=", employee)
		if workflow := get_workflow("Essdee Permission Application"):
			allowed_states = get_allowed_states_for_workflow(workflow, approver_id)
			filters[workflow.workflow_state_field] = ("in", allowed_states)
		else:
			filters.status = "Open"
			filters.permission_approver = approver_id
	else:
		filters.docstatus = ("!=", 2)
		filters.employee = employee

	return filters

@frappe.whitelist()
def get_personal_permission_balance(employee: str):
	from datetime import datetime , timedelta
	from frappe.utils import get_last_day,nowdate,getdate
	perm_doc = frappe.qb.DocType("Essdee Permission Application")
	query = (
		frappe.qb.from_(perm_doc)
		.select('name')
		.where(
			(perm_doc.posting_date.between(datetime.today().replace(day=1),get_last_day(nowdate()))) &
			(perm_doc.employee == employee) &
			(perm_doc.status == 'Approved') &
			(perm_doc.permission_type == 'Personal Permission')
		)
	)
	perm_list = query.run()
	doc = frappe.get_single('Essdee Attendance Settings')
	return doc.personal_permission_limit - len(perm_list)

@frappe.whitelist()
def get_permission_approval_details(employee: str) -> dict:
	leave_approver, department = frappe.get_cached_value(
		"Employee",
		employee,
		["leave_approver", "department"],
	)

	if not leave_approver and department:
		leave_approver = frappe.db.get_value(
			"Department Approver",
			{"parent": department, "parentfield": "leave_approvers", "idx": 1},
			"approver",
		)

	leave_approver_name = frappe.db.get_value("User", leave_approver, "full_name", cache=True)
	department_approvers = get_department_approvers(department, "leave_approvers")

	if leave_approver and leave_approver not in [approver.name for approver in department_approvers]:
		department_approvers.append({"name": leave_approver, "full_name": leave_approver_name})

	return dict(
		permission_approver=leave_approver,
		permission_approver_name=leave_approver_name,
		department_approvers=department_approvers,
		is_mandatory=frappe.db.get_single_value(
			"HR Settings", "leave_approver_mandatory_in_leave_application"
		),
	)
