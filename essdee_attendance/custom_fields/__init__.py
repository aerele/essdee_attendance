import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from essdee_attendance.custom_fields.employee import employee_fields
from essdee_attendance.custom_fields.attendance import attendance_fields
from essdee_attendance.custom_fields.shift_type import shift_type_fields
from essdee_attendance.custom_fields.department import department_fields
from essdee_attendance.custom_fields.branch import branch_fields

def make_custom_fields():
    custom_fields = {
        'Employee': employee_fields,
        'Attendance': attendance_fields,
        'Shift Type': shift_type_fields,
        'Department': department_fields,
		'Branch': branch_fields,
    }
    create_custom_fields(custom_fields, ignore_validate=frappe.flags.in_patch, update=True)