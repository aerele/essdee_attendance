attendance_fields = [
    {
        "fieldname": "sd_no_of_shifts",
        "fieldtype": "Float",
        "label": "No of Shifts",
        "insert_after": "shift",
        "allow_on_submit":True,
        "precision": 2
    },
    {
        "fieldname": "sd_general_shifts",
        "fieldtype": "Float",
        "label": "General Shifts",
        "insert_after": "sd_no_of_shifts",
        "allow_on_submit":True,
        "read_only":True,
        "precision": 2
    },
    {
        "fieldname": "sd_ot_shifts",
        "fieldtype": "Float",
        "label": "OT Shifts",
        "insert_after": "sd_general_shifts",
        "allow_on_submit":True,
        "read_only":True,
        "precision": 2
    }
]