// Copyright (c) 2024, Aerele and contributors
// For license information, please see license.txt
frappe.query_reports["Essdee Permission Application"] = {
	"filters": [
		{
			'fieldname': 'start_date',
			'fieldtype': 'Date',
			'label': 'Start Date',
			'default' : frappe.datetime.month_start(),
		},
		{
			'fieldname': 'end_date',
			'fieldtype': 'Date',
			'label': 'End Date',
			'default' : frappe.datetime.month_end(),
		},
		{
			"fieldname":"employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee",
		},
		{
			"fieldname" : "permission_type",
			"label" : __("Permission Type"),
			"fieldtype":"Select",
			"options":"\nPersonal Permission\nOn Duty"
		},
		{
			"fieldname":"department",
			"label": __("Department"),
			"fieldtype": "Link",
			"options": "Department",
		},
		{
			'fieldname': 'summary',
			'fieldtype': 'Check',
			'label': 'Summary',
		}
	],
};
