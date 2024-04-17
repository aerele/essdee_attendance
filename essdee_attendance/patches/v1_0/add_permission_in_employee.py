from frappe.permissions import add_permission, update_permission_property

def execute():
    add_permission("Employee", "Production Data Entry", permlevel=0, ptype='select')
    update_permission_property("Employee", "Production Data Entry", 0, 'read', 0)
    update_permission_property("Employee", "Production Data Entry", 0, 'export', 0)