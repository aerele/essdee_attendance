// Copyright (c) 2024, Aerele and contributors
// For license information, please see license.txt

frappe.query_reports["Essdee Advance Balance"] = {
	"filters": [
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_days(frappe.datetime.week_end(), -1),
			"reqd":1
		},
		{
			"fieldname":"employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee",
			get_query: () => {
				var department = frappe.query_report.get_filter_value('department');
				return {
					filters: {
						'department': department,
					}
				};
			}
		},
		{
			"fieldname" : "type",
			"label" : __("Type"),
			"fieldtype":"Select",
			"options":"\nAdvance\nPay Later",
			"default":"Advance",
		},
		{
			"fieldname":"department",
			"label": __("Department"),
			"fieldtype": "Link",
			"options": "Department",
		}
	]
};
