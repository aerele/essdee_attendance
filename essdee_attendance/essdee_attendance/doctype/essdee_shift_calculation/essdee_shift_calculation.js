// Copyright (c) 2025, Aerele and contributors
// For license information, please see license.txt
let filter = null
frappe.ui.form.on("Essdee Shift Calculation", {
	refresh(frm) {
        frm.set_df_property("essdee_shift_calculation_extra_ot_details","cannot_add_rows",true)
        frm.set_df_property("essdee_shift_calculation_extra_ot_details","cannot_delete_rows",true)
        let field1 = false
        let filterGroup = frm.fields_dict["filters_html"].$wrapper;
        let x = frm.doc.filters_json
        x = !x ? [] : JSON.parse(x)
        if(!filter){
            frappe.model.with_doctype("Employee", () => {
                filter = new frappe.ui.FilterGroup({
                    parent: filterGroup,
                    doctype: "Employee",
                });
                for(let i = 0 ; i < x.length; i++){
                    filter.push_new_filter(x[i], true)
                }
            });
        }
        if(!frm.doc.frozen){
            frm.add_custom_button("Freeze", function(){
                let d = new frappe.ui.Dialog({
                    title: "Are you want to freeze this document",
                    primary_action_label:"Yes",
                    secondary_action_label:"No",
                    primary_action(){
                        d.hide()
                        frm.doc.frozen = 1;
                        frm.refresh_field("frozen")
                        frm.dirty()
                        frm.save()
                    },
                    secondary_action(){
                        d.hide()
                    }
                })
                d.show()
            })
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
        }
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
    apply_filter: function(frm) {
        if(!frm.doc.frozen){
            let filters = filter.get_filters();
            frm.doc.filters_json = JSON.stringify(filters)
            frm.dirty()
            frm.save()
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
    },
    validate(frm){
        if(!frm.doc.frozen){
            let filters = filter.get_filters();
            frm.doc.filters_json = JSON.stringify(filters)
        }
    },
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
