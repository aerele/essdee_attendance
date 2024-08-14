# Copyright (c) 2024, Aerele and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import get_datetime, time_diff_in_hours, get_timedelta, getdate
from erpnext.stock.utils import get_combine_datetime
from datetime import datetime, timedelta

def execute(filters=None):
	columns, data = [], []
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_columns(filters):
	columns =[
		{
			'fieldname': 'employee',
			'fieldtype': 'Link',
			'label': 'Employee',
			"options": "Employee",
		},
		{
			'fieldname':'full_name',
			'fieldtype': 'Data',
			'label': 'Name',
			'width':150
		},
		{
			'fieldname': 'department',
			'fieldtype': 'Link',
			'label': 'Department',
			"options": "Department",
		},
		{
			'fieldname': 'designation',
			'fieldtype': 'Link',
			'label': 'Designation',
			"options": "Designation",
			'width':120
		},
		{
			'fieldname':'permission_type',
			'fieldtype': 'Data',
			'label': 'Permission Type',
			'width':120
		},
	]
	if not filters.summary:
		columns.extend([
			{
				'fieldname':'permission_approver',
				'fieldtype': 'Link',
				'label': 'Permission Approver',
				'options': 'User',
				'width':120
			},
			{
				'fieldname': 'status',
				'fieldtype': 'Select',
				'label': 'Status',
				'options':"\nOpen\nApproved\nRejected",
			},
			{
				'fieldname':'start_date',
				'fieldtype': 'Date',
				'label': 'Start Date',
			},
			{
				'fieldname':'start_time',
				'fieldtype': 'Time',
				'label': 'Start Time',
			},
			{
				'fieldname':'end_date',
				'fieldtype': 'Date',
				'label': 'End Date',
			},
			{
				'fieldname':'end_time',
				'fieldtype': 'Time',
				'label': 'End Time',
			},
			{
				'fieldname':'purpose',
				'fieldtype': 'Data',
				'label': 'Purpose',
				'width':120
			}
		])
	else:
		columns.extend([
			{
				'fieldname':'total_permissions',
				'fieldtype':'Float',
				'label':'Total Permissions',
				'precision': 2,
				'width': 150,
			},
			{
				'fieldname': 'total_permission_hours',
				'fieldtype':'Float',
				'label':'Total Permission Hours',
				'precision':2,
				'width': 150,
			}
		])	
	
	return columns

def get_data(filters):
	permissions = frappe.qb.DocType('Essdee Permission Application')
	query = frappe.qb.from_(permissions).select('*')
	if filters.employee:
		query = query.where(permissions.employee == filters.employee)
	
	if filters.permission_type:
		query = query.where(permissions.permission_type == filters.permission_type)
	
	if filters.department:
		query = query.where(permissions.department == filters.department)
	
	if filters.start_date:
		query = query.where(permissions.start_date >= filters.start_date)
	
	if filters.end_date:
		query = query.where(permissions.end_date <= filters.end_date)	
	
	if not filters.summary:
		result = query.run(as_dict = True)	
		return result
	else:
		query = query.where(permissions.status == 'Approved')
		result = query.run(as_dict=True)
		summary_result = {}
		for res in result:
			if not summary_result.get(res.employee, False):
				summary_result[res.employee] = []
				x = get_details(res)				
				summary_result[res.employee].append(x)			
			else:
				same_permission_type = False
				index = -1
				
				for ind,x in enumerate(summary_result[res.employee]):
					if x['permission_type'] == res.permission_type:
						same_permission_type = True
						index = ind
						break

				if same_permission_type:
					if res.start_date == res.end_date:
						diff = time_diff_in_hours(res.end_time, res.start_time)
						summary_result[res.employee][index]['total_permissions'] += 1
						summary_result[res.employee][index]['total_permission_hours'] += diff
					else:
						shift_type = frappe.get_value("Employee", {'name': res.employee}, 'default_shift')
						starts,ends = frappe.get_value("Shift Type", {'name': shift_type}, ['start_time','end_time'])
						summary_result[res.employee][index]['total_permissions'] += 1
						summary_result[res.employee][index]['total_permission_hours'] += time_diff_in_hours(ends, res.start_time)
						start_date = res.start_date + timedelta(days=1)
						while True:
							if start_date == res.end_date:
								summary_result[res.employee][index]['total_permission_hours'] += time_diff_in_hours(res.end_time, starts)
								break
							else:
								summary_result[res.employee][index]['total_permission_hours'] += time_diff_in_hours(ends, starts)
								start_date = start_date + timedelta(days=1)
				else:
					x = get_details(res)
					summary_result[res.employee].append(x)
		final_result = []	
		for key, value in summary_result.items():
			for val in value:
				decimal = val['total_permission_hours'] - int(val['total_permission_hours'])
				point = (60/100)* decimal
				if round(point,2) == 0.6:
					point = 1
				val['total_permission_hours'] = int(val['total_permission_hours']) + point	
				final_result.append(val)
		return final_result


	
def get_details(res):
	x = {
		"employee": res.employee,
		'full_name': res.full_name,
		"department" : res.department,
		"designation" : res.designation,
		"permission_type" : res.permission_type,
	}
	if res.start_date == res.end_date:
		diff = time_diff_in_hours(res.end_time, res.start_time)
		x['total_permissions'] = 1
		x['total_permission_hours'] = diff
	else:
		shift_type = frappe.get_value("Employee", {'name': res.employee}, 'default_shift')
		starts,ends = frappe.get_value("Shift Type", {'name': shift_type}, ['start_time','end_time'])
		start_date = res.start_date
		x['total_permissions'] = 1
		x['total_permission_hours'] = time_diff_in_hours(ends, res.start_time)
		while True:
			if start_date == res.end_date:
				x['total_permission_hours'] += time_diff_in_hours(res.end_time, starts)
				break
			else:
				x['total_permission_hours'] += time_diff_in_hours(ends, starts)
				start_date = start_date + timedelta(days=1)
	return x			
	
	
