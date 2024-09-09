// Copyright (c) 2024, Aerele and contributors
// For license information, please see license.txt

frappe.query_reports["Essdee Advance Balance"] = {
	"filters": [
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd":1
		},
		{
			"fieldname":"employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee",
		},
		{
			"fieldname" : "type",
			"label" : __("Type"),
			"fieldtype":"Select",
			"options":"\nAdvance\nPay Later\nMonthly Salary",
			"default":"Advance",
		},
		// {
		// 	"fieldname":"department",
		// 	"label": __("Department"),
		// 	"fieldtype": "Link",
		// 	"options": "Department",
		// }
	]
};
