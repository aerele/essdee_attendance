import frappe
from frappe import _

def execute(filters=None):
	columns, data = [],[]
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_columns(filters):
	columns = [
		{'fieldname': 'employee_id', 'fieldtype': 'Data', 'label': 'Employee ID', 'options': 'Employee','width':180},
		{'fieldname': 'employee_name', 'fieldtype': 'Data', 'label': 'Employee Name','width':180},
		{'fieldname': 'operation', 'fieldtype': 'Data', 'label': 'Operation','width':180},
		{'fieldname': 'quantity', 'fieldtype': 'Int', 'label': 'Quantity','width':100},
		{'fieldname': 'total', 'fieldtype': 'Currency', 'label': 'Total','width':180}
	]
	if not filters.summarized_view:
		columns.insert(3, {'fieldname': 'rate', 'fieldtype': 'Currency', 'label': 'Rate','width':100})
	return columns

def get_data(filters):
	data = []
	# fil = {}
	# filter_keys = ['employee', 'default_shift', 'employment_type', 'branch', 'department', 'company']
	# for key in filter_keys:
	# 	if key in filters and filters[key] is not None:
	# 		fil[key] = filters[key]

	# docs = frappe.get_all('Employee',filters=fil,fields=['name'])
	# for doc in docs:
	# 	doc = frappe.get_list('Essdee Work Entry',filters={'employee':doc.name,'date': ['between', [filters['from_date'], filters['to_date']]]},fields=['name'])
	# 	for detail in doc:
	# 		parent_doc = frappe.get_doc("Essdee Work Entry",detail['name'])
	# 		for row in parent_doc.details:
	# 			table_data = row.as_dict()
	# 			employee_details = {
	# 				'employee_id': parent_doc.employee,
	# 				'employee_name': frappe.get_value('Employee',parent_doc.employee,'employee_name'),
	# 				'operation': table_data.operation,
	# 				'rate': table_data.rate,
	# 				'quantity': table_data.quantity,
	# 				'total': table_data.total
	# 			}
	# 			if not filters.summarized_view:	
	# 				existing_entry = next((item for item in data if item['employee_id'] == employee_details['employee_id'] and item['operation'] == employee_details['operation']), None)
	# 				if existing_entry:
	# 					existing_entry['quantity'] += employee_details['quantity']
	# 					existing_entry['total'] = existing_entry['quantity']*existing_entry['rate']
	# 				else:
	# 					data.append(employee_details)
	# 			else:
	# 				employee_details.pop('rate')
	# 				existing_entry = next((item for item in data if item['employee_id'] == employee_details['employee_id']), None)
	# 				if existing_entry:
	# 					existing_entry['quantity'] += employee_details['quantity']
	# 					existing_entry['total'] += employee_details['total']
	# 					if employee_details['operation'] not in existing_entry['operation']:
	# 						existing_entry['operation'] += "," + employee_details['operation']
	# 				else:
	# 					data.append(employee_details)

	Essdee_Work_Entry = frappe.qb.DocType('Essdee Work Entry')
	Essdee_Work_Entry_Detail = frappe.qb.DocType('Essdee Work Entry Detail')
	Employee = frappe.qb.DocType('Employee')
	query = frappe.qb.from_(Essdee_Work_Entry).join(Essdee_Work_Entry_Detail) \
		.on(Essdee_Work_Entry.name == Essdee_Work_Entry_Detail.parent)
	
	query = query.join(Employee).on(Essdee_Work_Entry.employee == Employee.name)

	query = query.select(
			Employee.name,
			Employee.employee_name,
			Essdee_Work_Entry_Detail.operation,
			Essdee_Work_Entry_Detail.rate,
			Essdee_Work_Entry_Detail.quantity,
			Essdee_Work_Entry_Detail.total,
		).where(Essdee_Work_Entry.date.between(filters.from_date, filters.to_date))
	
	if filters.employee:
		query = query.where(Essdee_Work_Entry.employee == filters.employee)
	if filters.employment_type:
		query= query.where(Employee.employment_type == filters.employment_type)
	if filters.department:
		query= query.where(Employee.department == filters.department)
	if filters.default_shift:
		query= query.where(Employee.default_shift == filters.default_shift)
	if filters.branch:
		query= query.where(Employee.branch == filters.branch)

	query = query.orderby(Employee.name)			 
	result = query.run(as_dict = True)
	for row in result:
		employee_details = {
			'employee_id': row.name,
			'employee_name': row.employee_name,
			'operation': row.operation,
			'rate': row.rate,
			'quantity': row.quantity,
			'total': row.total
		}
		if not filters.summarized_view:	
			existing_entry = next((item for item in data if item['employee_id'] == employee_details['employee_id'] and item['operation'] == employee_details['operation']), None)
			if existing_entry:
				existing_entry['quantity'] += employee_details['quantity']
				existing_entry['total'] = existing_entry['quantity']*existing_entry['rate']
			else:
				data.append(employee_details)
		else:
			employee_details.pop('rate')
			existing_entry = next((item for item in data if item['employee_id'] == employee_details['employee_id']), None)
			if existing_entry:
				existing_entry['quantity'] += employee_details['quantity']
				existing_entry['total'] += employee_details['total']
				if employee_details['operation'] not in existing_entry['operation']:
					existing_entry['operation'] += "," + employee_details['operation']
			else:
				data.append(employee_details)
	return data
