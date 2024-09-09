shift_type_fields = [
    {
        "fieldname": "sd_enable_essdee_attendance",
        "fieldtype": "Check",
        "label": "Enable Essdee Attendance",
        "insert_after": "enable_auto_attendance"
    },
    {
        "fieldname": "sd_essdee_attendance_settings",
        "label": "Essdee Attendance Settings",
        "fieldtype": 'Section Break',
        "insert_after": "sd_enable_essdee_attendance",
        "depends_on": "sd_enable_essdee_attendance"
    },
    {
        "fieldname": "sd_allowed_early_entry",
        "fieldtype": "Int",
        "label": "Allowed Early Entry (In Mins)",
        "insert_after": "sd_essdee_attendance_settings"
    },
    {
        "fieldname": "sd_shift_time_mapping",
        "fieldtype": "Table",
        "label": "Shift Time Mapping",
        "options": "Shift Time Mapping",
        "insert_after": "sd_allowed_early_entry"
    }
]