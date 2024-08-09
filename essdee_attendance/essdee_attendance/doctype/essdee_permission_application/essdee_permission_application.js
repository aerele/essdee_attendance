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
    refresh(frm){
        if(frm.doc.permission_approver == frappe.session.user && frm.doc.status == 'Open'){
            frm.page.add_menu_item(__("Approve"), function() {
                let d = new frappe.ui.Dialog({
                    title: "Are you sure want to approve this permission ?",
                    primary_action_label: 'Yes',
                    secondary_action_label: 'No',
                    primary_action() {
                        frm.set_value("status",'Approved')
                        // frm.set_value("docstatus",1);
                        frm.doc.docstatus = 1;
                        frm.save().then(()=>{
    						frappe.show_alert({ message: __("Permission Approved"), indicator: "green" });
                        })
                        d.hide()

    
                    },
                    secondary_action() {
                        d.hide();
                    }
                });
                
                d.show();
                
            });
            frm.page.add_menu_item(__("Reject"), function(){
                let d = new frappe.ui.Dialog({
                    title: "Are you sure want to reject this permission ?",
                    primary_action_label:'Yes',
                    secondary_action_label:"NO",
                    primary_action(){
                        frm.set_value('status','Rejected')
                        frm.save().then(()=>{
    						frappe.show_alert({ message: __("Permission Rejected"), indicator: "red" });
                        })
                        d.hide()
                    },
                    secondary_action(){
                        d.hide()
                    }
                })
                d.show()
            })
        }
    },
    employee(frm){
        if(frm.doc.employee){
            frappe.call({
                method:'essdee_attendance.essdee_attendance.doctype.essdee_permission_application.essdee_permission_application.get_employee_details',
                args:{
                    employee: frm.doc.employee,
                },
                callback: function(res){
                    frm.set_value('department', res.message.department);
                    frm.set_value('designation', res.message.designation);
                    frm.set_value('full_name', res.message.full_name);
                    frm.set_value("permission_approver",res.message.leave_approver);
                }
            })
        }
        else{
            frm.set_value('department','');
            frm.set_value('designation','');
            frm.set_value('full_name','');
            frm.set_value('permission_approver','');
        }
    },
    permission_type(frm){
        frm.set_value('start_date',null)
        frm.set_value('start_time',null)
        frm.set_value('end_date',null)
        frm.set_value('end_time',null)
    },
    start_time(frm){
        if(frm.doc.start_time){
            if(frm.doc.permission_type == 'Personal Permission'){
                let s = frm.doc.start_time.split(":")
                if(s[0] < 13){
                    frappe.msgprint("Permission is not applicable for morning shift");
                    frm.set_value('start_time', null)
                    return;
                }
                else{
                    frm.trigger('validate_start_and_end_datetime');
                }
            }
            else{
                frm.trigger('validate_start_and_end_datetime');
            }
        }    
    },
    validate_start_and_end_datetime(frm){
        frappe.call({
            method:'essdee_attendance.essdee_attendance.doctype.essdee_permission_application.essdee_permission_application.valid_start_and_end_datetime',
            args: {
                'start_time': frm.doc.start_time,
                'employee': frm.doc.employee,
                'type': frm.doc.permission_type
            },
            callback:function(r){
                if(!r.message.start){
                    frm.set_value("start_time",r.message.start)
                }
                frm.set_value('end_time',r.message.end)
            }
        })
    },
    end_time(frm){
        if(frm.doc.end_time){
            if(frm.doc.permission_type != "Personal Permission"){
                frappe.call({
                    method:'essdee_attendance.essdee_attendance.doctype.essdee_permission_application.essdee_permission_application.valid_endtime',
                    args: {
                        'end_time': frm.doc.end_time,
                        'employee': frm.doc.employee,
                    },
                    callback:function(r){
                        if(!r.message){
                            frm.set_value('end_time',r.message)
                        }
                    }
                })
            }
        }
    },
    start_date(frm){
        if(frm.doc.start_date){
            if(frm.doc.permission_type == 'Personal Permission'){
                frm.set_value('end_date',frm.doc.start_date)
            }
        }
    }
});