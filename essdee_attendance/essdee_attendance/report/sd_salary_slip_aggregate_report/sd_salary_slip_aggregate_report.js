// Copyright (c) 2025, Aerele and contributors
// For license information, please see license.txt

frappe.query_reports["SD Salary Slip Aggregate Report"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"fieldtype":"Date",
			"label":"From Date",
			"default":frappe.datetime.add_months(frappe.datetime.month_start(), -1)
		},
		{
			"fieldname":"to_date",
			"fieldtype":"Date",
			"label":"To Date",
			"default":frappe.datetime.add_days(frappe.datetime.month_start(), -1)
		},
		{
			"fieldname":"salary_slip_method",
			"fieldtype":"Select",
			"label":"Salary Slip Method",
			"options":"\nRegular\nPay Later\nMonthly Salary",
			"default":"Regular"
		}
	]
};
