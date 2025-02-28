// Copyright (c) 2024, Aerele and contributors
// For license information, please see license.txt

frappe.query_reports["SD Weekly Wages Summary"] = {
	"filters": [
		{
			"fieldname": "report_date",
			"label": __("Report Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.datetime.now_date(),
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
		{
			"fieldname": "salary_batch",
			"label": __("Salary Batch"),
			"fieldtype": "Link",
			"options": "SD Salary Batch",
		},
		{
			"fieldname":"method",
			"label":__("Method"),
			"fieldtype":"Select",
			"options":"\nRegular\nPay Later\nMonthly Salary\nMonthly Salary - Pay\nStaff Salary\nOthers",
			"default":"Regular"
		},
		{
			"fieldname":"hide_zero_amount",
			"label":__("Hide Zero Amount"),
			"fieldtype":"Check",
			"default":1,
		}
	]
};
