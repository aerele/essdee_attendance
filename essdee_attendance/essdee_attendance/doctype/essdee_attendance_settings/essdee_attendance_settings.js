// Copyright (c) 2020, Aerele and contributors
// For license information, please see license.txt

frappe.ui.form.on('Essdee Attendance Settings', {
	// refresh: function(frm) {

	// }
	update_shift_to_attendance: function() {
		frappe.call({
			method: "essdee_attendance.essdee_attendance.doctype.essdee_attendance_settings.essdee_attendance_settings.update_shift_to_attendance",
			freeze: true,
			callback: function(r) {
				frappe.msgprint(__("Attendance updated successfully"))
			}
		})
	},
	sync_all: function() {
		frappe.call({
			method: "essdee_attendance.essdee_attendance.doctype.essdee_attendance_settings.essdee_attendance_settings.sync_records"
		})
	}
});
