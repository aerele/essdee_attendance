// Copyright (c) 2021, Aerele and contributors
// For license information, please see license.txt

frappe.ui.form.on('Essdee Biometric Device', {
	sync_now: function(frm){
		frappe.call({
			method: "essdee_attendance.essdee_attendance.doctype.essdee_attendance_settings.essdee_attendance_settings.sync_records",
			args: {doc:frm.doc},
			freeze: true
		})
	}
});
