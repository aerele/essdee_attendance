// Copyright (c) 2024, Aerele and contributors
// For license information, please see license.txt

frappe.ui.form.on("SD Salary Slip", {
	refresh: function(frm) {

	},

    salary_amount: function(frm) {
        calculate_all(frm)
    },

    other_additions: function(frm) {
        calculate_all(frm)
    },

    advance: function(frm) {
        calculate_all(frm)
    },

    canteen: function(frm) {
        calculate_all(frm)
    },

    esi_pf: function(frm) {
        calculate_all(frm)
    },

    other_deductions: function(frm) {
        calculate_all(frm)
    },

    leave: function(frm) {
        calculate_all(frm)
    },

    via_cash: function(frm) {
        calculate_all(frm)
    },

    method: function(frm) {
        calculate_all(frm)
    },
});

function calculate_all(frm) {
    frm.doc.total_deductions = (get_float(frm.doc.advance) + get_float(frm.doc.canteen) + get_float(frm.doc.esi_pf) + get_float(frm.doc.other_deductions) + get_float(frm.doc.leave) + get_float(frm.doc.via_cash))
    let total = get_float(frm.doc.salary_amount) + (get_float(frm.doc.other_additions)) - (get_float(frm.doc.total_deductions));
    if (frm.doc.method == "Pay Later") {
        frm.doc.pay_later_amount = total;
        frm.doc.total_amount = 0;
    } else {
        frm.doc.pay_later_amount = 0;
        frm.doc.total_amount = total;
    }
    frm.refresh_field("total_deductions");
    frm.refresh_field("pay_later_amount");
    frm.refresh_field("total_amount");
}

function get_float(x) {
    return Number(x) || 0;
}
