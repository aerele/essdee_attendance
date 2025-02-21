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
        "fieldname":"section_break_sd_details",
        "fieldtype":"Section Break",
        "collapsible":True,
        "label":"SD Details",
        "insert_after":"early_exit",
    },
    {
        "fieldname": "sd_general_shifts",
        "fieldtype": "Float",
        "label": "General Shifts",
        "insert_after": "section_break_sd_details",
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
    },
    {
        "fieldname": "sd_shift_rate",
        "fieldtype": "Currency",
        "label": "Shift Rate",
        "insert_after": "sd_ot_shifts",
        "precision": 2
    },
    {
        "fieldname": "sd_shift_wages",
        "fieldtype": "Currency",
        "label": "Shift Wages",
        "insert_after": "sd_shift_rate",
        "precision": 2
    },
    {
        "fieldname": "sd_minimum_wages",
        "fieldtype": "Currency",
        "label": "Minimum Wages",
        "insert_after": "sd_shift_wages",
        "precision": 2
    }
]