// Copyright (c) 2020, Aerele and contributors
// For license information, please see license.txt

frappe.ui.form.on('Essdee Attendance Settings', {
	// refresh: function(frm) {

	// }
	update_attendance: function() {
		frappe.call({
			method: "essdee_attendance.essdee_attendance.doctype.essdee_attendance_settings.essdee_attendance_settings.update_attendance",
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

frappe.ui.form.on("Device Details", {
	sync_now: function(frm, cdt, cdn) {
		frappe.call({
			method: "essdee_attendance.essdee_attendance.doctype.essdee_attendance_settings.essdee_attendance_settings.sync_records",
			args: {row:frm.selected_doc}
		})
	}
});
