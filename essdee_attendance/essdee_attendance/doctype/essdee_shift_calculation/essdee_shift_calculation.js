// Copyright (c) 2025, Aerele and contributors
// For license information, please see license.txt

frappe.ui.form.on("Essdee Shift Calculation", {
	refresh(frm) {
        frm.set_df_property("essdee_shift_calculation_details","cannot_add_rows",true)
        frm.set_df_property("essdee_shift_calculation_details","cannot_delete_rows",true)
        frm.add_custom_button("Calculate", function(){
            frappe.call({
                method:"essdee_attendance.essdee_attendance.doctype.essdee_shift_calculation.essdee_shift_calculation.calculate_wages",
                args: {
                    doc_name : frm.doc.name
                },
                callback: function(r){
                    frm.reload_doc()
                }
            })
        })
	},
});
