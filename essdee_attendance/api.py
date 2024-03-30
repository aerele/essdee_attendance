import frappe,json

@frappe.whitelist(allow_guest=True)
def get_employees(**args):
    # join_date = args['selected_date']
    fields = ['name', 'first_name'] 
    employees = frappe.get_list('Employee', fields=fields)
    return employees

@frappe.whitelist(allow_guest=True)
def get_selected_employees(**args):
    employees = args.get('employees', [])
    employees = json.loads(employees)
    fields = ['name', 'first_name', 'last_name', 'gender', 'date_of_birth', 'status', 'company', 'department','person_to_be_contacted','blood_group','emergency_phone_number','image'] 
    employee_data = []
    for employee in employees:
        employee_details = frappe.get_list('Employee',filters={'name': employee}, fields=fields)
        if employee_details:
            employee_data.append(employee_details)
    return employee_data


@frappe.whitelist(allow_guest=True)
def get_employees_by_department(**args):
    department = args['department']
    company = args['company']
    fields = ['name','first_name']
    if company and department:
        employees = frappe.get_list('Employee', filters={'department': department,'company':company}, fields=fields)
    elif department:
        employees = frappe.get_list('Employee', filters={'department': department}, fields=fields)
    elif company:
        employees = frappe.get_list('Employee', filters={'company':company}, fields=fields)        
    return employees

@frappe.whitelist(allow_guest=True)
def store_employees(**args):
    employees = args['Employees']
    employees = json.loads(employees)
    doc = frappe.get_single('Employee ID Card')
    doc.child_table=[]
    for emp in employees:
        for employee in emp:
            name = employee['name']
            first_name = employee['first_name']
            last_name = employee['last_name']
            gender = employee['gender']
            date_of_birth = employee['date_of_birth']
            status = employee['status']
            company = employee['company']
            department = employee['department']
            person_to_be_contacted = employee['person_to_be_contacted']
            blood_group = employee['blood_group']
            emergency_phone_number = employee['emergency_phone_number']
            image = employee['image']
        doc.append('child_table',{'employee_id':name,'first_name':first_name,'gender':gender,'date_of_birth':date_of_birth,'status':status,'company':company,'department':department,'person_to_be_contacted':person_to_be_contacted,'blood_group':blood_group,'emergency_phone_number':emergency_phone_number,'image':image})
        doc.save(ignore_permissions=True) 
        frappe.db.commit() 



