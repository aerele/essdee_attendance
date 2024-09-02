import frappe
from hrms.api import get_workflow, get_workflow_state_field, get_allowed_states_for_workflow, get_department_approvers

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
