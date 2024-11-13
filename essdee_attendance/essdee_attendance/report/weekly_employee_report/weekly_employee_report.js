// Copyright (c) 2016, Aerele and contributors
// For license information, please see license.txt
/* eslint-disable */

let cur_cell_height = 1;
function get_cell_height(rows) {
	let cellHeights = [33, 33, 50, 66, 83]
	if (rows < 0 ) {
		return 33;
	} else if (rows >= 0 && rows < cellHeights.length) {
		return cellHeights[rows]
	} else {
		return 83;
	}
}


function set_cell_height() {
	if (!frappe.query_report.datatable) return;
	let rows = get_rows();
	if (rows != cur_cell_height) {
		frappe.query_report.datatable.options.cellHeight = get_cell_height(rows);
		// frappe.query_report.datatable.refresh(frappe.query_report.data, frappe.query_report.columns)
	}
	cur_cell_height = rows;
}

function get_rows() {
	if (frappe.query_report.get_filter_value('summarized_view')) return 1;
	let rows = 0;
	let x = ['show_in_out', 'show_time_logs', 'show_hours', 'show_shift'];
	for (let i = 0; i < x.length; i++) {
		if (frappe.query_report.get_filter_value(x[i])) {
			rows += 1;
		}
	}
	return rows || 1;
}

frappe.query_reports["Weekly Employee Report"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.datetime.add_days(frappe.datetime.week_start(), -2)
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.datetime.add_days(frappe.datetime.week_end(), -2)
		},
		{
			"fieldname":"employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee",
			get_query: () => {
				var company = frappe.query_report.get_filter_value('company');
				return {
					filters: {
						'company': company
					}
				};
			}
		},
		{
			"fieldname":"employment_type",
			"label": __("Employment Type"),
			"fieldtype": "Link",
			"options": "Employment Type",
		},
		{
			"fieldname":"shift",
			"label": __("Shift"),
			"fieldtype": "Link",
			"options": "Shift Type",
		},
		{
			"fieldname":"branch",
			"label": __("Branch"),
			"fieldtype": "Link",
			"options": "Branch",
		},
		{
			"fieldname":"department",
			"label": __("Department"),
			"fieldtype": "Link",
			"options": "Department",
		},
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"reqd": 1
		},
		{
			"fieldname":"summarized_view",
			"label": __("Summarized View"),
			"fieldtype": "Check",
			"default": 0,
			on_change: () => {
				set_cell_height();
				frappe.query_report.refresh();
			}
		},
		{
			"fieldname":"show_in_out",
			"label": __("Show In Out"),
			"fieldtype": "Check",
			"default": 1,
			on_change: () => {
				set_cell_height();
				frappe.query_report.refresh();
			}
		},
		{
			"fieldname":"show_time_logs",
			"label": __("Show Time Logs"),
			"fieldtype": "Check",
			"default": 0,
			on_change: () => {
				set_cell_height();
				frappe.query_report.refresh();
			}
		},
		{
			"fieldname":"show_hours",
			"label": __("Show Hours"),
			"fieldtype": "Check",
			"default": 1,
			on_change: () => {
				set_cell_height();
				frappe.query_report.refresh();
			}
		},
		{
			"fieldname":"show_shift",
			"label": __("Show Shift"),
			"fieldtype": "Check",
			"default": 1,
			on_change: () => {
				set_cell_height();
				frappe.query_report.refresh();
			}
		},
		{
			"fieldname":"status",
			"label": __("Employment Status"),
			"fieldtype": "Select",
			"options": "\nActive\nInactive",
			"default": "Active",
		},
	],

	get_datatable_options(options) {
		let rows = get_rows();
		return Object.assign(options, {
			cellHeight: get_cell_height(rows),
		})
	},
}
