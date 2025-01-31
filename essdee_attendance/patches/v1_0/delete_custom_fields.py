import frappe

def execute():
    custom_field_list = frappe.get_list("Custom Field", filters={"dt":"Employee","fieldname":"sd_attendance_book_serial"},pluck="name")
    try:
        frappe.delete_doc("Custom Field",custom_field_list[0])
        print("Custom Field Deleted")
    except:    
        print("Custom Field is Already Deleted")