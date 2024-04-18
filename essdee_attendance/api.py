import frappe,json

@frappe.whitelist()
def get_employees(**args):
    fields = ['name', 'employee', 'first_name', 'employee_name'] 
    employees = frappe.get_list('Employee', fields=fields)
    return employees

@frappe.whitelist()
def get_selected_employees(**args):
    employees = args.get('employees')
    employees = json.loads(employees)
    fields = ['name', 'first_name', 'last_name', 'gender', 'date_of_birth', 'status', 'company', 'department','person_to_be_contacted','blood_group','emergency_phone_number','image','sd_signature_upload','father_or_spouse','relation'] 
    temp = frappe.get_list('Employee',filters={'name': ['in', employees]}, fields=fields)
    return temp

@frappe.whitelist()
def get_employees_by_filters(**args):
    filters = args["filters"]
    fields = ['name', 'employee', 'first_name', 'employee_name'] 
    employees = frappe.get_list('Employee',filters=filters, fields=fields)
    return employees

@frappe.whitelist()
def store_employees(**args):
    employees = args['Employees']
    employees = json.loads(employees)
    doc = frappe.get_single('Employee ID Card')
    doc.child_table=[]
    print(employees)
    for employee in employees:
        doc.append('child_table',{
            'employee_id':employee['name'],
            'first_name':employee['first_name'],
            'gender':employee['gender'],
            'date_of_birth':employee['date_of_birth'],
            'status':employee['status'],
            'company':employee['company'],
            'department':employee['department'],
            'person_to_be_contacted':employee['person_to_be_contacted'],
            'father_or_spouse':employee['father_or_spouse'],
            'blood_group':employee['blood_group'],
            'emergency_phone_number':employee['emergency_phone_number'],
            'image':employee['image'],
            'sd_signature_upload':employee['sd_signature_upload'],
            'relation': employee['relation']
        })
    doc.save(ignore_permissions=True) 
    return True



