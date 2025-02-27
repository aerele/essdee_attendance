// Copyright (c) 2024, Aerele and contributors
// For license information, please see license.txt

frappe.ui.form.on("Essdee Advance Entry", {
	refresh(frm){
        if(frm.doc.docstatus == 1 && !frm.doc.downloaded_time){
            frm.add_custom_button("Download Bank File", ()=> {
                get_xl(frm.doc.name)
            })
        }
    }
});

frappe.ui.form.on("Essdee Advance Entry Detail", {
	employee(frm, cdt, cdn){
        let row = frappe.get_doc(cdt, cdn)
        if(row.employee){
            frappe.db.get_value("Employee", row.employee, "salary_mode").then((r)=> {
                row.salary_mode = r.message.salary_mode
                frm.refresh_field("essdee_advance_entry_details")
            })
        }
    }
});

function get_xl(doc_name){
	var xhr = new XMLHttpRequest();	
    xhr.open('POST', '/api/method/essdee_attendance.essdee_attendance.doctype.essdee_advance_entry.essdee_advance_entry.download_entries', true);
	xhr.setRequestHeader('X-Frappe-CSRF-Token',frappe.csrf_token)
	xhr.responseType = 'arraybuffer';
	xhr.onload = function (success) {
		if (this.status === 200) {
			var blob = new Blob([success.currentTarget.response], {type: "application/xlsx"});
			var filename = ""
			var disposition = xhr.getResponseHeader('Content-Disposition');
			if (disposition && disposition.indexOf('filename') !== -1) {
				var filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
				var matches = filenameRegex.exec(disposition);
				if (matches != null && matches[1]) filename = matches[1].replace(/['"]/g, '');
			}
	
			if (typeof window.navigator.msSaveBlob !== 'undefined') {
				window.navigator.msSaveBlob(blob, filename);
			} else {
				var URL = window.URL || window.webkitURL;
				var downloadUrl = URL.createObjectURL(blob);
	
				if (filename) {
					var a = document.createElement("a");
					if (typeof a.download === 'undefined') {
						window.location.href = downloadUrl;
					} else {
						a.href = downloadUrl;
						a.download = filename;
						document.body.appendChild(a);
						a.click();
					}
				} else {
					window.location.href = downloadUrl;
				}
	
				setTimeout(function () { URL.revokeObjectURL(downloadUrl); }, 100); // cleanup
			}
		}
		else{
            frappe.msgprint("Error")
		}
	};
	xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	xhr.send($.param({doc_name : doc_name}, true));
}
