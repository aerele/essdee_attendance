import frappe

def execute(filters=None):
	columns, data = [],[]
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_columns(filters):
	columns = [
		{'fieldname': 'employee_id', 'fieldtype': 'Data', 'label' : 'Employee ID', 'options' : 'Employee',},
		{'fieldname': 'employee_name', 'fieldtype': 'Data','label' : 'Employee Name',},
		{'fieldname': 'operation', 'fieldtype': 'Data', 'label' : 'Operation',},
	]
	if not filters.summarized_view:
		columns.extend([
			{'fieldname': 'rate', 'fieldtype': 'Data', 'label' : 'Rate',}
		])
	columns.extend([
		{'fieldname': 'quantity','fieldtype': 'Data','label' : 'Quantity',},
		{'fieldname': 'total','fieldtype': 'Data','label' : 'Total',},
	])	
	return columns

def get_data(filters):
	data = []
	fil = filters.copy()
	fil.pop('from_date')
	fil.pop('to_date')
	if fil.summarized_view:
		fil.pop('summarized_view')
	docs = frappe.get_all('Employee',filters=fil,fields=['name'])	
	for doc in docs:
		doc = frappe.get_list('Essdee Work Entry',filters={'employee':doc.name},fields=['employee','date','name'])
		for d in doc:
			parent_doc = frappe.get_doc("Essdee Work Entry",d['name'])
			for row in parent_doc.details:
				table_data = row.as_dict()
				m = {
					'employee_id': parent_doc.employee,
					'employee_name': frappe.get_value('Employee',parent_doc.employee,'employee_name'),
					'operation': table_data.operation,
					'rate': table_data.rate,
					'quantity': table_data.quantity,
					'total': table_data.total
				}
				if not filters.summarized_view:	
					existing_entry = next((item for item in data if item['employee_id'] == m['employee_id'] and item['operation'] == m['operation']), None)
					if existing_entry:
						existing_entry['quantity'] += m['quantity']
						existing_entry['total'] = existing_entry['quantity']*existing_entry['rate']
					else:
						data.append(m)
				else:
					m.pop('rate')
					existing_entry = next((item for item in data if item['employee_id'] == m['employee_id']), None)
					if existing_entry:
						existing_entry['quantity'] += m['quantity']
						existing_entry['total'] += m['total']
						if m['operation'] not in existing_entry['operation']:
							existing_entry['operation'] += "," + m['operation']
					else:
						data.append(m)					
	return data
