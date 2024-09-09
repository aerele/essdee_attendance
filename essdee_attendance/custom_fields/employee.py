
overview_tab_fields = [
    {
        "fieldname": "nick_name",
        "fieldtype": "Data",
        "label": "Nick Name",
        "insert_after": "first_name",
    },
    {
        "fieldname": "sd_shift_rate",
        "fieldtype": "Currency",
        "label": "Shift Rate",
        "description": "Allocate rate per shift",
        "insert_after": "date_of_joining",
        "precision": 2
    },
    {
        'fieldname':'sd_nature_of_employee',
        'fieldtype':'Select',
        'options':'Permanent\nTemporary\nContract',
        'label':"Nature of Employee",
        'insert_after':'salutation',
        'default':'Permanent',
    },
    {
        "fieldname": "sd_attendance_book_serial",
        "fieldtype": "Data",
        "label": "Attendance Book Serial",
        "insert_after": "employment_type",
        "unique": 1,
    },
    {
        "fieldname": "sd_salary_batch",
        "fieldtype": "Link",
        "label": "Salary Batch",
        "options": "SD Salary Batch",
        "insert_after": "sd_attendance_book_serial",
    },
    {
        'fieldname':'essdee_employee_operations',
        "fieldtype":'Table',
        'label': 'Essdee Employee Operations',
        'options': 'Essdee Employee Operation',
        'insert_after':'employee_number'
    },
    {
        'fieldname':'sd_branch_title',
        'fieldtype':'Data',
        'label':'Branch Address Title',
        'insert_after':'branch',
        'read_only': True,
        'fetch_from': 'branch.branch_address_title'
    },
    {
        'fieldname':'sd_branch_address',
        'fieldtype':'Long Text',
        'label':"Branch Address",
        'insert_after':'sd_branch_title',
        'read_only': True,
        'fetch_from': 'branch.branch_address'
    },
    {
        'fieldname':'hostel',
        "fieldtype":'Check',
        'label': 'Hostel',
        'insert_after':'sd_branch_address'
    },
    {
        'fieldname':'canteen',
        "fieldtype":'Check',
        'label': 'Canteen',
        'insert_after':'hostel'
    },
    {
        'fieldname':'hostel_room_number',
        "fieldtype":'Data',
        'label': 'Hostel Room Number',
        'insert_after':'canteen'
    },
]

address_tab_fields = [
    {
        "fieldname": "father_or_spouse",
        "fieldtype": "Data",
        "label": "Father/Spouse",
        "reqd": True,
        "insert_after": "cell_number",
    },
    {
        "fieldname": "company_mobile",
        "fieldtype": "Data",
        "label": "Company Mobile Number",
        "insert_after": "father_or_spouse",
    },
    {
        'fieldname':'sd_cell_number_2',
        'fieldtype':'Data',
        'label':'Mobile Number 2',
        'insert_after':'column_break_40',
        'read_only': 0,
    },
    {
        "fieldname": "relation_",
        "fieldtype": "Select",
        "label": "Relation",
        "reqd": 1,
        "options": "\nFather\nMother\nSpouse\nBrother\nSister\nChild\nOther",
        "insert_after": "relation",
    },
]

attendance_tab_fields = [
    {
        "fieldname": "work_location",
        "fieldtype": "Table",
        "label": "Work Location",
        "options": "Work Location",
        "insert_after": "attendance_device_id"
    },
    {
        "fieldname": "finger_print_details",
        "fieldtype": "Table",
        "label": "Finger Print Details",
        "options": "Finger Print Details",
        "insert_after": "work_location",
        "read_only": 1
    },
    {
        "fieldname": "enroll_fingerprint",
        "depends_on": "eval: !doc.__islocal",
        "fieldtype": "Button",
        "label": "Enroll Fingerprint",
        "insert_after": "default_shift"
    },
    {
        "fieldname": "sync_now",
        "depends_on": "eval: !doc.__islocal",
        "fieldtype": "Button",
        "label": "Sync Now",
        "insert_after": "enroll_fingerprint"
    },
    {
        "fieldname": "shift_request_approver",
        "fieldtype": "Link",
        "options": "User",
        "label": "Shift Request Approver",
        "insert_after": "column_break_45"
    },
]

salary_tab_fields = [
    {
        "fieldname": "sd_default_salary_slip_method",
        "fieldtype": "Select",
        "label": "Default Salary Slip Method",
        "options": "Regular\nPay Later\nMonthly Salary",
        "insert_after": "salary_mode",
        "default": "Regular",
    },
    {
        "fieldname": "sd_bank_account_name",
        "fieldtype": "Data",
        "label": "Bank Account Name",
        "insert_after": "bank_name",
    },
    {
        "fieldname": "sd_bank_account_status",
        "fieldtype": "Select",
        "label": "Bank Account Status",
        "options": "\nPending Approval\nApproved",
        "depends_on": "eval:doc.salary_mode == \"Bank\"",
        "insert_after": "bank_ac_no",
    },
    {
        "fieldname": "custom_section_break_dajzs",
        "fieldtype": "Section Break",
        "label": "Uploads",
        "insert_after": "iban",
    },
    {
        'fieldname':'sd_cheque_leaf_upload',
        'fieldtype':'Attach Image',
        'label':'Upload Cheque Leaf',
        'insert_after':'custom_section_break_dajzs',
    },
    {
        'fieldname':'sd_passbook_upload',
        'fieldtype':'Attach Image',
        'label':'Upload Passbook',
        'insert_after':'sd_cheque_leaf_upload',
    },
]

personal_tab_fields = [
    {
        "fieldname": "compliance_details",
        "fieldtype": "Section Break",
        "label": "Compliance Details",
        "insert_after": "health_details",
    },
    {
        "fieldname": "sd_aadhaar_no",
        "fieldtype": "Data",
        "label": "Aadhar No",
        "reqd": True,
        "insert_after": "compliance_details",
    },
    {
        "fieldname": "sd_pf",
        "fieldtype": "Data",
        "label": "PF",
        "insert_after": "sd_aadhaar_no",
    },
    {
        "fieldname": "sd_pan",
        "fieldtype": "Data",
        "label": "PAN",
        "insert_after": "sd_pf",
    },
    {
        "fieldname": "sd_name_as_per_pan",
        "fieldtype": "Data",
        "label": "Name as PER PAN",
        "insert_after": "sd_pan",
    },
    {
        'fieldname':'column_break_106',
        'fieldtype':'Column Break',
        'label':"",
        'insert_after':'sd_name_as_per_pan',
    },
    {
        "fieldname": "sd_uan",
        "fieldtype": "Data",
        "label": "UAN",
        "insert_after": "column_break_106",
    },
    {
        "fieldname": "sd_esic",
        "fieldtype": "Data",
        "label": "ESIC",
        "insert_after": "sd_uan",
    },
    {
        "fieldname": "sd_esi_employee_dispensary",
        "fieldtype": "Data",
        "label": "ESI Employee Dispensary",
        "insert_after": "sd_esic",
    },
    {
        "fieldname": "sd_esi_family_dispensary",
        "fieldtype": "Data",
        "label": "ESI Family Dispensary",
        "insert_after": "sd_esi_employee_dispensary",
    },
    {
        "fieldname": "sd_family_details_break",
        "fieldtype": "Section Break",
        "label": "Family Details",
        "insert_after": "sd_esi_family_dispensary",
    },
    {
        "fieldname": "sd_family_details",
        "fieldtype": "Table",
        "label": "Family Details",
        'options':'SD Family Details',
        "insert_after": "sd_family_details_break",
    },
    {
        "fieldname": "upload_documents",
        "fieldtype": "Section Break",
        "label": "Upload Documents",
        "insert_after": "sd_family_details",
    },
    {
        'fieldname':'sd_aadhaar_upload',
        'fieldtype':'Attach Image',
        'label':'Upload Aadhar Front',
        'insert_after':'upload_documents',
    },
    {
        'fieldname':'sd_aadhar_back_upload',
        'fieldtype':'Attach Image',
        'label':'Upload Aadhar Back',
        'insert_after':'sd_aadhaar_upload',
    },
    {
        'fieldname':'column_break_116',
        'fieldtype':'Column Break',
        'label':"",
        'insert_after':'sd_aadhar_back_upload',
    },
    {
        'fieldname':'sd_pan_upload',
        'fieldtype':'Attach Image',
        'label':'Upload PAN',
        'insert_after':'column_break_116',
    },
    {
        'fieldname':'sd_signature_upload',
        'fieldtype':'Attach Image',
        'label':'Upload Signature',
        'insert_after':'sd_pan_upload',
    },
    {
        "fieldname": "sd_remarks_section",
        "fieldtype": "Section Break",
        "label": "",
        "insert_after": "sd_signature_upload",
    },
    {
        "fieldname": "sd_hr_remarks",
        "fieldtype": "Long Text",
        "label": "HR Remarks (Internal)",
        "insert_after": "sd_remarks_section",
    },
]

exit_tab_fields = [
    {
        "fieldname": "sd_resignation_acceptance_date",
        "fieldtype": "Date",
        "label": "Resignation Acceptance Date",
        "insert_after": "resignation_letter_date",
    },
    {
        "fieldname": "sd_resignation_letter",
        "fieldtype": "Attach Image",
        "label": "Resignation Letter",
        "insert_after": "encashment_date",
    },
]


employee_fields = overview_tab_fields + address_tab_fields + attendance_tab_fields + salary_tab_fields + personal_tab_fields + exit_tab_fields