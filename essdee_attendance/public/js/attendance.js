
frappe.ui.form.on("Attendance", {
	refresh(frm){
		let user_roles = frappe.user_roles
		let index = user_roles.indexOf("HR Manager")
		if(index == -1){
			frm.set_df_property("sd_shift_rate","hidden",true)
		}
		else{
			frm.set_df_property("sd_shift_rate","hidden",false)
		}
	},
});