import frappe
from frappe.utils import flt
from datetime import datetime

@frappe.whitelist()
def trial_expired():
    return False


def create_advance_ledger_entry(employee, posting_date, posting_time, amount, entry_type, transaction_type, transaction_name,running_balance):
    new_doc = frappe.new_doc('Essdee Advance Ledger Entry')
    new_doc.employee = employee
    new_doc.posting_date = posting_date
    new_doc.posting_time = posting_time
    new_doc.amount = amount
    new_doc.type = entry_type
    new_doc.transaction_type = transaction_type
    new_doc.transaction_name = transaction_name
    new_doc.running_balance = running_balance
    new_doc.save()

@frappe.whitelist()
def make_ledger(args, doctype):
    if doctype == 'EssdeeAdvanceEntry':
        for d in args.essdee_advance_entry_details:
            check_last_past_records(d.employee,args.posting_date,args.posting_time,args.posting_datetime,d.amount,d.type,"Essdee Advance Entry",args.name)
    else:
        if args.method == 'Pay Later':
            check_last_past_records(args.employee,args.posting_date,args.posting_time,args.posting_datetime,args.total_amount,"Pay Later","SD Salary Slip",args.name)
        if args.advance:
            amount = flt(args.advance)*flt(-1)
            check_last_past_records(args.employee,args.posting_date,args.posting_time,args.posting_datetime,amount,"Advance","SD Salary Slip",args.name)
            
def check_last_past_records(employee, posting_date, posting_time,posting_datetime, amount, entry_type, doctype, docname):
    doc = frappe.db.sql(
        """
        SELECT *
        FROM `tabEssdee Advance Ledger Entry`
        WHERE employee = %s
            AND type = %s
            AND (
                posting_datetime < %s
            )
        ORDER BY posting_datetime DESC limit 1""",
        (employee,entry_type,posting_datetime),
        as_dict=True,
    )
    if doc:
        doc = doc[0] 
        running_balance = flt(doc.running_balance) + flt(amount) 
        if running_balance >= 0:
            check_future_records(employee, posting_date, posting_time,posting_datetime, amount, entry_type, doc.running_balance,doctype,docname)
        else:
            frappe.throw("Can't insert these values")
    else:
        if amount >= 0:
            check_future_records(employee, posting_date, posting_time,posting_datetime, amount, entry_type,0,doctype,docname)
        else:
            frappe.throw("Can't insert these values")
    

def check_future_records(employee, posting_date, posting_time,posting_datetime, amount, entry_type, running_balance,doctype, docname):
    posting_date = datetime.strptime(posting_date, "%Y-%m-%d").date()
    docs = frappe.db.sql(
        """
        SELECT *
        FROM `tabEssdee Advance Ledger Entry`
        WHERE employee = %s
            AND type = %s
            AND (
                posting_datetime > %s
            )
        ORDER BY posting_datetime ASC""",
        (employee,entry_type,posting_datetime),
        as_dict=True,
    )
    if not docs:
        running_balance = flt(amount) + flt(running_balance)
        create_advance_ledger_entry(employee,posting_date,posting_time,amount,entry_type,doctype,docname,running_balance)
    else:
        x = flt(amount)+flt(running_balance)
        for doc in docs:
            s = flt(doc.amount) + flt(x)
            if s < 0:
                frappe.throw("Can't insert these values")
            else:
                x = s

        new_entry_running_balance = flt(amount)+flt(running_balance)
        create_advance_ledger_entry(employee,posting_date,posting_time,amount,entry_type,doctype,docname,new_entry_running_balance)
        for doc in docs:
            d = frappe.get_doc("Essdee Advance Ledger Entry",doc.name)
            s = flt(d.amount) + flt(new_entry_running_balance)
            d.running_balance = s
            new_entry_running_balance = s
            d.save()

@frappe.whitelist()
def cancel_ledger(transaction_name, transaction_type):
    docs = frappe.get_all('Essdee Advance Ledger Entry',filters={'transaction_type': transaction_type, 'transaction_name':transaction_name})
    for doc in docs:
        d = frappe.get_doc('Essdee Advance Ledger Entry',doc.name)
        d.is_cancelled = True
        d.save()
