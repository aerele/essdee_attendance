// Copyright (c) 2024, Aerele and contributors
// For license information, please see license.txt

frappe.ui.form.on("Time Card Generator", {
	refresh(frm) {
        frm.add_custom_button("Re-Generate", ()=> {
            frappe.call({
				method: 'essdee_attendance.essdee_attendance.doctype.time_card_generator.time_card_generator.update_time_card_timing',
				args: {
					import_file: frm.doc.upload_file,
				},
				freeze:true,
				freeze_message: __("Re-Generating Time Cards..."),
			})
        })
        frm.add_custom_button("Generate", ()=> {
            frappe.call({
				method: 'essdee_attendance.essdee_attendance.doctype.time_card_generator.time_card_generator.create_time_card_timing',
				args: {
					import_file: frm.doc.upload_file,
				},
				freeze:true,
				freeze_message: __("Generating Time Cards...")
			})
        })
		frm.add_custom_button("Print", ()=> {
			frappe.call({
				method:"essdee_attendance.essdee_attendance.doctype.time_card_generator.time_card_generator.get_time_card_datas",
				callback: function(r){
					if(r.message){
						const sitename = window.location.origin;
						const printFormatURL = `${sitename}${r.message}`;
						window.open(printFormatURL, "_blank");
					}
				}
			})
		})
	},
});
