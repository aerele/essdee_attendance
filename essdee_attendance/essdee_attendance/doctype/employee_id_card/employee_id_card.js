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
        frm.add_custom_button('Print', () => addFields(wrapper))
        var filterWrapper = frm.fields_dict["filter_area"].$wrapper;
        filterWrapper.html('');
        let filter_group = new frappe.ui.FilterGroup({
            parent: filterWrapper,
            doctype: "Employee",
        })
        frappe.model.with_doctype("Employee", () => {
            filter_group.refresh();
        });       
        frm.add_custom_button('Apply Filters', () => {
            let filters = filter_group.get_filters();
            fetchEmployeesWithFilters(filters, wrapper);
        });
    },
    select_all: function(frm) {
        var wrapper = frm.fields_dict["employee_list"].$wrapper;
        selectAllEmployees(wrapper);
    },
    unselect_all: function(frm) {
        var wrapper = frm.fields_dict["employee_list"].$wrapper;
        unselectAllEmployees(wrapper);
    }        
});

function fetchEmployeesWithFilters(filters,wrapper) {
    frappe.call({
        method: "essdee_attendance.api.get_employees_by_filters",
        args: {
            'filters': filters,
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
    console.log(selectedEmployees)
    if(selectedEmployees.length > 0){
        frappe.call({
            method:"essdee_attendance.api.store_employees",
            args:{
                'Employees': selectedEmployees 
            },
        });
        const sitename = window.location.origin;
        const printFormatURL = `${sitename}/app/print/Employee%20ID%20Card`;
        window.open(printFormatURL, "_blank");
    }
    else{
        frappe.msgprint('No Employee was selected')
    }
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
    wrapper.find('input[type="checkbox"]').prop('checked', false);
}
async function showSelectedEmployee(wrapper) {
    const selectedEmployees = [];
    wrapper.find('input[type="checkbox"]').each(function() {
        if ($(this).prop('checked')) {
            const employeeName = $(this).val();
            selectedEmployees.push(employeeName);
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
                } else {
                    frappe.msgprint("Failed to fetch employees.");
                }
            }
        });
    }
    return sendEmployee;
}





