// Copyright (c) 2024, Aerele and contributors
// For license information, please see license.txt

frappe.query_reports["SD Weekly Wages Summary"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.datetime.week_start(),
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.datetime.week_end(),
		},
		{
			"fieldname": "employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee",
		},
		{
			"fieldname": "department",
			"label": __("Department"),
			"fieldtype": "Link",
			"options": "Department",
		},
		{
			"fieldname": "employment_type",
			"label": __("Employment Type"),
			"fieldtype": "Link",
			"options": "Employment Type",
		},
		{
			"fieldname": "designation",
			"label": __("Designation"),
			"fieldtype": "Link",
			"options": "Designation",
		},
		{
			"fieldname": "branch",
			"label": __("Branch"),
			"fieldtype": "Link",
			"options": "Branch",
		},
		{
			"fieldname": "salary_mode",
			"label": __("Salary Mode"),
			"fieldtype": "Select",
			"options": "\nBank\nCash",
		},
	]
};
