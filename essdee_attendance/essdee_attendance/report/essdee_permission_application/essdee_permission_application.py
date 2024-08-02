# Copyright (c) 2024, Aerele and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_columns():
	columns =[
		{
			'fieldname': 'employee',
			'fieldtype': 'Link',
			'label': 'Employee',
			"options": "Employee",
			'width':170
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
			'width':120
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
		{
			'fieldname':'permission_approver',
			'fieldtype': 'Link',
			'label': 'Permission Approver',
			'options': 'User',
			'width':120
		},
		{
			'fieldname':'start_date',
			'fieldtype': 'Date',
			'label': 'Start Date',
			'width':100
		},
		{
			'fieldname':'start_time',
			'fieldtype': 'Time',
			'label': 'Start Time',
			'width':100
		},
		{
			'fieldname':'end_date',
			'fieldtype': 'Date',
			'label': 'End Date',
			'width':100
		},
		{
			'fieldname':'end_time',
			'fieldtype': 'Time',
			'label': 'End Time',
			'width':100
		},
		{
			'fieldname':'purpose',
			'fieldtype': 'Data',
			'label': 'Purpose',
			'width':120
		}
	]
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

	# query = query.orderby(permissions.posting_datetime, order=Order.desc)	
	result = query.run(as_dict = True)	
	return result
