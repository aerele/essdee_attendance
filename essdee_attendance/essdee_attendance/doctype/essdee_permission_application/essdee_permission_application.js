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
    refresh:(frm)=>{
        const is_permission_approver = frm.doc.permission_approver && frm.doc.permission_approver == frappe.session.user;
        const is_status_open = frm.doc.status === 'Open';
        const is_leave_approver = !frm.doc.permission_approver && frappe.user.has_role('Leave Approver');

        if((is_permission_approver && is_status_open) || (is_leave_approver && is_status_open)){
            frm.page.add_menu_item(__("Approve"), function() {
                let d = new frappe.ui.Dialog({
                    title: "Are you sure want to approve this permission ?",
                    primary_action_label: 'Yes',
                    secondary_action_label: 'No',
                    primary_action() {
                        frappe.show_alert({ message: __("Permission Approved"), indicator: "green" });
                        frappe.call({
                            method:'essdee_attendance.essdee_attendance.doctype.essdee_permission_application.essdee_permission_application.submit_doc',
                            args: {
                                doc_name: frm.doc.name,
                                status: 'Approved',
                            }
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
                        frappe.show_alert({ message: __("Permission Rejected"), indicator: "red" });
                        frappe.call({
                            method:'essdee_attendance.essdee_attendance.doctype.essdee_permission_application.essdee_permission_application.submit_doc',
                            args: {
                                doc_name: frm.doc.name,
                                status: 'Rejected',
                            }
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
        if(frm.doc.status == 'Open' && frm.doc.permission_approver){
            frm.add_custom_button("Notify", ()=> {
                frappe.call({
                    method:'essdee_attendance.essdee_attendance.doctype.essdee_permission_application.essdee_permission_application.send_email',
                    args: {
                        doc_name: frm.doc.name
                    }
                })
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
                    frm.set_value('employee_name', res.message.employee_name);
                    frm.set_value("permission_approver",res.message.leave_approver);
                }
            })
        }
        else{
            frm.set_value('department','');
            frm.set_value('designation','');
            frm.set_value('employee_name','');
            frm.set_value('permission_approver','');
        }
    },
    // permission_type(frm){
    //     if(frm.doc.permission_type == 'Personal Permission' && frm.doc.start_time){
    //         frm.trigger('start_time')
    //         frm.set_value('end_date',frm.doc.start_date)
    //         frm.set_value('end_time',null)
    //         frm.trigger('validate_start_and_end_datetime')
    //     }
    // },
    // start_time(frm){
    //     if(frm.doc.start_time){
    //         if(frm.doc.permission_type == 'Personal Permission'){
    //             let s = frm.doc.start_time.split(":")
    //             if(s[0] < 13){
    //                 frappe.msgprint("Permission is not applicable for morning shift");
    //                 frm.set_value('start_time', null)
    //                 return;
    //             }
    //             else{
    //                 frm.trigger('validate_start_and_end_datetime');
    //             }
    //         }
    //         else{
    //             frm.trigger('validate_start_and_end_datetime');
    //         }
    //     }    
    // },
    // validate_start_and_end_datetime(frm){
    //     frappe.call({
    //         method:'essdee_attendance.essdee_attendance.doctype.essdee_permission_application.essdee_permission_application.valid_start_and_end_datetime',
    //         args: {
    //             'start_time': frm.doc.start_time,
    //             'employee': frm.doc.employee,
    //             'type': frm.doc.permission_type
    //         },
    //         callback:function(r){
    //             if(r.message.start){
    //                 frm.set_value("start_time",r.message.start)
    //             }
    //             if(r.message.end){
    //                 frm.set_value('end_time',r.message.end)
    //             }
    //             if(r.message.msg){
    //                 frappe.show_alert({ message: r.message.msg, indicator: "red" })
    //             }
    //         }
    //     })
    // },
    // end_time(frm){
    //     if(frm.doc.end_time){
    //         if(frm.doc.permission_type != "Personal Permission"){
    //             frappe.call({
    //                 method:'essdee_attendance.essdee_attendance.doctype.essdee_permission_application.essdee_permission_application.valid_endtime',
    //                 args: {
    //                     'end_time': frm.doc.end_time,
    //                     'employee': frm.doc.employee,
    //                 },
    //                 callback:function(r){
    //                     if(r.message.end){
    //                         frm.set_value('end_time',r.message.end)
    //                     }
    //                     if(r.message.msg){
    //                         frappe.show_alert({message: r.message.msg, indicator: "red"})
    //                     }
    //                 }
    //             })
    //         }
    //     }
    // },
    // start_date(frm){
    //     if(frm.doc.start_date){
    //         if(frm.doc.permission_type == 'Personal Permission'){
    //             frm.set_value('end_date',frm.doc.start_date)
    //         }
    //     }
    // }
});
