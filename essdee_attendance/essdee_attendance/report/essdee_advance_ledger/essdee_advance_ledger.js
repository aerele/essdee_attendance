// Copyright (c) 2024, Aerele and contributors
// For license information, please see license.txt

frappe.query_reports["Essdee Advance Ledger"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_days(frappe.datetime.get_today(), -30)
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
		},
		{
			"fieldname" : "type",
			"label" : __("Type"),
			"fieldtype":"Select",
			"options":"\nAdvance\nPay Later"
		},
		{
			"fieldname":"department",
			"label": __("Department"),
			"fieldtype": "Link",
			"options": "Department",
		},
	],
	formatter: function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (column.fieldname == "amount") {
			if (data.amount >= 0) {
				value = "<span style='color:green'>" + value + "</span>";
			} 
			else if (data.amount < 0) {
				value = "<span style='color:red'>" + value + "</span>";
			} 
		}
		return value
	}
};	
