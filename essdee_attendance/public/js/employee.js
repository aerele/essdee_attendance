frappe.ui.form.on("Employee", {
	refresh(frm){
		let user_roles = frappe.user_roles
		let index = user_roles.indexOf("HR Manager")
		if(index == -1 || frm.doc.employment_type != "Shift"){
			frm.set_df_property("sd_shift_rate","hidden",true)
			frm.set_df_property("sd_shift_wages","hidden", true)
		}
	},
    enroll_fingerprint: function(frm){
		let d = new frappe.ui.Dialog({
			title: __('Enroll Fingerprint'),
			fields: [
				{ fieldtype: 'Link', options: 'Essdee Biometric Device', reqd: 1, fieldname: 'select_biometric_device', label: 'Select Biometric Device'},
			],
			primary_action_label: __('Enroll'),
			primary_action: function() {
				frm.enable_save();
				frappe.call({
					method: "essdee_attendance.essdee_attendance.doctype.essdee_attendance_settings.essdee_attendance_settings.enroll_fingerprint",
					freeze: true, args: {doc: frm.doc, device: d.get_value('select_biometric_device')},
					callback: function(r) {
						if(r.message) {
							var val = frm.add_child('finger_print_details');
							val['id'] = r.message[0];
							val['template'] = r.message[1];
						}
						refresh_field('finger_print_details');
						frappe.msgprint(__("Successfully Enrolled"));
						frm.save();
					}
				});
				d.hide();
			}
		});
		d.show();
    },
	employment_type(frm){
		let user_roles = frappe.user_roles
		let index = user_roles.indexOf("HR Manager")
		if(index == -1 || frm.doc.employment_type != "Shift"){
			frm.set_df_property("sd_shift_rate","hidden",true)
			frm.set_df_property("sd_shift_wages","hidden", true)
		}
	},
    sync_now: function(frm){
		frappe.call({
			method: "essdee_attendance.essdee_attendance.doctype.essdee_attendance_settings.essdee_attendance_settings.sync_now",
			args: {employee:frm.doc},
			freeze: true
		})
	},
});