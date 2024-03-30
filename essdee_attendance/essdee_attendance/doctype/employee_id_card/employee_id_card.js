frappe.ui.form.on("Employee ID Card", {
    refresh(frm) {
        var wrapper = frm.fields_dict["employee_list"].$wrapper;
        wrapper.html('');
        frappe.call({
            method: "essdee_attendance.api.get_employees",
            callback: function(r) { 
                if (r.message) {
                    renderEmployeeList(r.message, wrapper);
                } else {
                    frappe.msgprint("Failed to fetch employees.");
                }
            }
        });
        frm.add_custom_button('Print',() => addFields(wrapper))
    }
});
frappe.ui.form.on("Employee ID Card", {
    department: function(frm) {
        let department = '';
        let company = '';
        if (frm.doc.company == null){
            company = null;
        }
        else{
            company=frm.doc.company;
        }
        if (frm.doc.department == null){
            department = null;
        }
        else{
            department=frm.doc.department;
        }
        const wrapper = frm.fields_dict["employee_list"].$wrapper;
        wrapper.empty();
        fetchEmployeesByDepartment(department, company, wrapper);
    },
    company: function(frm) {
        let company = '';
        let department = '';
        if (frm.doc.department == null){
            department = null;
        }
        else{
            department=frm.doc.department;
        }
        if (frm.doc.company == null){
            company = null;
        }
        else{
            company=frm.doc.company;
        }
        const wrapper = frm.fields_dict["employee_list"].$wrapper;
        wrapper.empty();
        fetchEmployeesByDepartment(department, company, wrapper);
    }
});

frappe.ui.form.on("Employee ID Card", "select_all", function(frm) {
    var wrapper = frm.fields_dict["employee_list"].$wrapper;
    selectAllEmployees(wrapper)
});
frappe.ui.form.on("Employee ID Card", "unselect_all", function(frm) {
    var wrapper = frm.fields_dict["employee_list"].$wrapper;
    unselectAllEmployees(wrapper)
});
frappe.ui.form.on("Employee ID Card", "unselect_all", function(frm) {
    var wrapper = frm.fields_dict["employee_list"].$wrapper;
    unselectAllEmployees(wrapper)
});

function fetchEmployeesByDepartment(department,company,wrapper) {
    frappe.call({
        method: "essdee_attendance.api.get_employees_by_department",
        args: {
            'department': department,
            'company': company,
        },
        callback: function(r) { 
            if (r.message) {
                wrapper.html("");
                renderEmployeeList(r.message,wrapper);
            } else {
                frappe.msgprint("No employees found for the selected date.");
            }
        }
    });
}
async function addFields(wrapper){
    const selectedEmployees =await showSelectedEmployee(wrapper);
    // console.log(selectedEmployees.length);
    if(selectedEmployees.length > 0){
        frappe.call({
            method:"essdee_attendance.api.store_employees",
            args:{
                'Employees': selectedEmployees 
            },
        });
    }
    const sitename = window.location.origin;
    const printFormatURL = `${sitename}/app/print/Employee%20ID%20Card`;
    window.open(printFormatURL, "_blank");
}
function renderEmployeeList(employees, wrapper) {
    employees.forEach(employee => {
        const checkbox = `<input type="checkbox" name="employee_checkbox" value="${employee.name}" />`;
        const label = `<label>${employee.first_name}</label>`;
        wrapper.append(`<div>${checkbox}${label}</div>`);
    });
}
function selectAllEmployees(wrapper) {
    wrapper.find('input[type="checkbox"]').prop('checked', true);
}
function unselectAllEmployees(wrapper) {
    // Find all checkboxes inside the wrapper and set them to unchecked
    wrapper.find('input[type="checkbox"]').prop('checked', false);
}
async function showSelectedEmployee(wrapper) {
    const selectedEmployees = [];
    wrapper.find('input[type="checkbox"]').each(function() {
        if ($(this).prop('checked')) {
            const employeeName = $(this).val();
            selectedEmployees.push(employeeName);  // Push the employeeName, not employeeDetails
        }
    });
    let sendEmployee = []
    if(selectedEmployees.length > 0){
        await frappe.call({
            method: 'essdee_attendance.api.get_selected_employees',
            args: {
                'employees': selectedEmployees,
            },
            callback: function(r) { 
                if (r.message) {
                    sendEmployee = r.message;
                    // console.log(sendEmployee)
                } else {
                    frappe.msgprint("Failed to fetch employees.");
                }
            }
        });
    }
    return sendEmployee;
}





