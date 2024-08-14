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
	formatter: function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (column.fieldname == "status") {
			if (data.status == 'Approved') {
				value = "<span style='color:green';>" + value + "</span>";
			} 
			else if (data.status == 'Rejected') {
				value = "<span style='color:red'>" + value + "</span>";
			}
			else if (data.status == 'Open'){
				value = "<span style='color:blue'>" + value + "</span>";
			} 
		}
		return value
	}
};
