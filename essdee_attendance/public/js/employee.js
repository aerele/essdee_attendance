frappe.ui.form.on("Employee", {
    refresh : (frm) => {
        if(!frm.doc.__islocal) {
        frm.add_custom_button(__("Delete Linked User"), function() {
            frm.trigger('delete_employee');
        });
    }
    },
    delete_employee: function(frm){
        frappe.call({
			method: "essdee_attendance.essdee_attendance.doctype.essdee_attendance_settings.essdee_attendance_settings.delete_employee",
			freeze: true,
            args: {id: frm.doc.attendance_device_id, work_location: frm.doc.work_location},
        }
        )
    }
});