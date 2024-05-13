// Copyright (c) 2024, Aerele and contributors
// For license information, please see license.txt

frappe.query_reports["Essdee Advance Ledger"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today()
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today()
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
			"options":"Advance\nPay Later"
		},
		{
			"fieldname":"department",
			"label": __("Department"),
			"fieldtype": "Link",
			"options": "Department",
		},
	]
};
