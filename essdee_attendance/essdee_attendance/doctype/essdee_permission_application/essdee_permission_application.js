// Copyright (c) 2024, Aerele and contributors
// For license information, please see license.txt

frappe.ui.form.on("Essdee Permission Application", {
    setup: function (frm) {
		frm.set_query("permission_approver", function () {
			return {
				query: "hrms.hr.doctype.department_approver.department_approver.get_approvers",
				filters: {
					employee: frm.doc.employee,
					doctype: frm.doc.doctype,
				},
			};
		});
	},
    employee(frm){
        if(frm.doc.employee){
            frappe.call({
                method:'essdee_attendance.essdee_attendance.doctype.essdee_permission_application.essdee_permission_application.get_dept_and_designation',
                args:{
                    employee: frm.doc.employee,
                },
                callback: function(res){
                    frm.set_value('department', res.message.department);
                    frm.set_value('designation', res.message.designation);
                    frm.set_value('full_name', res.message.full_name)
                }

            })
        }
        else{
            frm.set_value('department','');
            frm.set_value('designation','');
        }
    },
    permission_type(frm){
        frm.set_value('start_date',null)
        frm.set_value('start_time',null)
        frm.set_value('end_date',null)
        frm.set_value('end_time',null)
    },
    start_time(frm){
        if(!frm.doc.permission_type && frm.doc.start_time){
            frappe.msgprint("Please choose permission type before select the start time");
            frm.set_value('start_time', null)
            return
        }
        if(frm.doc.start_time){
            if(frm.doc.permission_type == 'Personal Permission'){
                let s = frm.doc.start_time.split(":")
                if(s[0] >= 16){
                    s[0] = '19'
                    s[1] = '00'
                    s[2] = '00'
                }
                else if(s[0] < 13){
                    frappe.msgprint("Permission is not applicable for morning shift");
                    frm.set_value('start_time', null)
                    return;
                }
                else{
                    s[0] = parseInt(s[0]) + 3;
                }
                let end_time = s.join(":")
                frm.set_value('end_time', end_time)
            }
        }
        else{
            frm.set_value('end_time',null)
        }    
    },
    start_date(frm){
        if(!frm.doc.permission_type && frm.doc.start_date){
            frappe.msgprint("Please choose permission type before select the start date");
            frm.set_value('start_date', null)
            return
        }
        if(frm.doc.start_date){
            if(frm.doc.permission_type == 'Personal Permission'){
                frm.set_value('end_date',frm.doc.start_date)
            }
        }
    }
});
