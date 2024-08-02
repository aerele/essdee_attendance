// Copyright (c) 2024, Aerele and contributors
// For license information, please see license.txt

frappe.query_reports["Essdee Permission Application"] = {
	"filters": [
		{
			"fieldname":"employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee",
			get_query: () => {
				var department = frappe.query_report.get_filter_value('department');
				if(!department){
					return
				}
				return {
					filters: {
						'department': department,
					}
				};
			}
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
	],
};
