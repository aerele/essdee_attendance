// Copyright (c) 2025, Aerele and contributors
// For license information, please see license.txt

frappe.ui.form.on("Essdee Shift Calculation", {
	refresh(frm) {
        frm.set_df_property("essdee_shift_calculation_extra_ot_details","cannot_add_rows",true)
        frm.set_df_property("essdee_shift_calculation_extra_ot_details","cannot_delete_rows",true)
        let field1 = false
        frm.add_custom_button("Calculate", function(){
            if(frm.doc.calculating == 1){
                frappe.msgprint("Already in the process")
                return
            }
            frm.trigger("load")
            field1 = true
            frappe.call({
                method:"essdee_attendance.essdee_attendance.doctype.essdee_shift_calculation.essdee_shift_calculation.calculate_wages",
                args: {
                    doc_name : frm.doc.name
                },
                callback: function(r){
                    console.log(r.message)
                    if(!r.message){
                        frm.doc.status = "Failed"
                        frm.doc.calculating = 0
                        frm.save()
                    }
                    frm.reload_doc()
                }
            })
        })
        frm.add_custom_button("Stop Calculating", ()=> {
            frm.doc.calculating = 0
            frm.dirty()
            frm.save()
        })
        if(frm.doc.calculating== 1){
            frm.set_df_property("start_date","read_only", true)
            frm.set_df_property("end_date","read_only", true)
            frm.set_df_property("shift_type","read_only", true)
            frm.trigger("load")
        }
        else{
            frm.set_df_property("start_date","read_only", false)
            frm.set_df_property("end_date","read_only", false)
            frm.set_df_property("shift_type","read_only", false)
            frm.trigger("stop_load")
        }
	},
    load(frm){
        const chartHTML = `<div class="loader"></div> `;
        const container = frm.fields_dict.calculation_loader.wrapper;
        container.innerHTML = chartHTML;
        const styleId = "custom-loader-style";
        if (!document.getElementById(styleId)) {
            const style = document.createElement("style");
            style.id = styleId;
            style.innerHTML = get_css();
            document.head.appendChild(style);
        }
    },
    stop_load(frm){
        const chartHTML = ``;
        const container = frm.fields_dict.calculation_loader.wrapper;
        container.innerHTML = chartHTML;
    }
});

function get_css(){
    return `
        .loader {
            margin-top:40px;
            border: 6px solid #f3f3f3; /* Light grey */
            border-top: 6px solid #3498db; /* Blue */
            border-radius: 50%;
            width: 30px;
            height: 30px;
            animation: spin 2s linear infinite;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    `
}
