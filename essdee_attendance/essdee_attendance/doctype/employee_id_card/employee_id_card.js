let filter_group = null;

frappe.ui.form.on("Employee ID Card", {
    refresh(frm) {
        let wrapper = frm.fields_dict["employee_list"].$wrapper;
        wrapper.html('');
        frappe.call({
            method: "essdee_attendance.api.get_employees",
            callback: function(r) { 
                if (r.message) {
                    renderEmployeeList(frm, r.message);
                } else {
                    frappe.msgprint("Failed to fetch employees.");
                }
            }
        });
        frm.disable_save();
        frm.add_custom_button('Print', () => addFields(frm))
        var filterWrapper = frm.fields_dict["filter_area"].$wrapper;
        filterWrapper.html('');
        filter_group = new frappe.ui.FilterGroup({
            parent: filterWrapper,
            doctype: "Employee",
        })
        frappe.model.with_doctype("Employee", () => {});
    },
    apply_filter: function(frm) {
        let filters = filter_group.get_filters();
        fetchEmployeesWithFilters(frm, filters);
    }     
});

function fetchEmployeesWithFilters(frm, filters) {
    frappe.call({
        method: "essdee_attendance.api.get_employees_by_filters",
        args: {
            'filters': filters,
        },
        callback: function(r) { 
            if (r.message) {
                renderEmployeeList(frm, r.message);
            } else {
                frappe.msgprint("No employees found for the selected date.");
            }
        }
    });
}

async function addFields(frm){
    const selectedEmployees = await getSelectedEmployee(frm);
    console.log(selectedEmployees)
    if(selectedEmployees.length > 0){
        frappe.call({
            method:"essdee_attendance.api.store_employees",
            args:{
                'Employees': selectedEmployees 
            },
            callback: function(r) {
                if (r.message) {
                    const sitename = window.location.origin;
                    const printFormatURL = `${sitename}/app/print/Employee%20ID%20Card`;
                    window.open(printFormatURL, "_self");
                }
            }
        });
    }
    else{
        frappe.msgprint('No Employee was selected')
    }
}

function renderEmployeeList(frm, employees) {
    const $wrapper = frm.get_field("employee_list").$wrapper;
    $wrapper.empty();
    const employee_wrapper = $(`<div class="employee_wrapper">`).appendTo($wrapper);
    console.log(employees)

    frm.employees_multicheck = frappe.ui.form.make_control({
        parent: employee_wrapper,
        df: {
            fieldname: "employees_multicheck",
            fieldtype: "MultiCheck",
            select_all: true,
            columns: 4,
            get_data: () => {
                return employees.map((employee) => {
                    return {
                        label: `${employee.employee} : ${employee.employee_name}`,
                        value: employee.employee,
                        checked: 0,
                    };
                });
            },
        },
        render_input: true,
    });

    frm.employees_multicheck.refresh_input();
}

async function getSelectedEmployee(frm) {
    const selectedEmployees = frm.employees_multicheck.get_checked_options();
    
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





