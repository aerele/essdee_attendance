import frappe,json
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
def make_ledger(detail_list):
    for row in detail_list:
        check_and_create_ledger(row['employee'],row['posting_date'],row['posting_time'],row['posting_datetime'],row['amount'],row['type'],row['doctype'],row['docname'])               

def check_and_create_ledger(employee,posting_date,posting_time,posting_datetime,amount,entry_type,doctype,docname):
    past_doc = get_last_past_record(employee,posting_datetime,entry_type)
    if past_doc:
        running_balance = flt(past_doc.running_balance) + flt(amount) 
        if running_balance >= 0:
            future_docs = get_future_records(employee, posting_datetime, entry_type)
            if future_docs:
                check_is_possible(running_balance,future_docs,employee,amount,entry_type)
                make_future_update(employee,posting_date,posting_time,amount,entry_type,doctype,docname,running_balance,future_docs,1)
            else:
                create_advance_ledger_entry(employee,posting_date,posting_time,amount,entry_type,doctype,docname,running_balance)
        else:
            frappe.throw(f'In {entry_type}, the amount {amount} is not applicable for {employee}')
    else:
        if amount >= 0:
            future_docs = get_future_records(employee,posting_datetime, entry_type)
            if future_docs:
                check_is_possible(amount,future_docs)
                make_future_update(employee,posting_date,posting_time,amount,entry_type,doctype,docname,0,future_docs,0)
            else:
                create_advance_ledger_entry(employee,posting_date,posting_time,amount,entry_type,doctype,docname,amount)
        else:
            frappe.throw(f'In {entry_type}, the amount {amount} is not applicable for {employee}')


def get_last_past_record(employee,posting_datetime, entry_type):
    doc = frappe.db.sql(
        """
        SELECT *
        FROM `tabEssdee Advance Ledger Entry`
        WHERE employee = %s
            AND type = %s
            AND (
                posting_datetime < %s
            )
            AND is_cancelled = 0
        ORDER BY posting_datetime DESC limit 1""",
        (employee,entry_type,posting_datetime),
        as_dict=True,
    )
    if doc:
        doc = doc[0] 
        return doc
    else:
        return None    

def get_future_records(employee,posting_datetime,entry_type):
    docs = frappe.db.sql(
        """
        SELECT *
        FROM `tabEssdee Advance Ledger Entry`
        WHERE employee = %s
            AND type = %s
            AND (
                posting_datetime > %s
            )
            AND is_cancelled = 0
        ORDER BY posting_datetime ASC""",
        (employee,entry_type,posting_datetime),
        as_dict=True,
    )
    if not docs:
        return None
    else:
        return docs

def check_is_possible(running_balance,docs,employee,amount,entry_type):
    x = flt(running_balance)
    for doc in docs:
        s = flt(doc.amount) + flt(x)
        if s < 0:
            frappe.throw(f'In {entry_type}, the amount {amount} is not applicable for {employee}')
        else:
            x = s

def make_future_update(employee,posting_date,posting_time,amount,entry_type,doctype,docname,running_balance,docs,check):
    new_entry_running_balance = 0
    if check == 0:
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
        employee = d.employee
        posting_datetime = d.posting_datetime
        entry_type = d.type
        past_doc = get_last_past_record(employee,posting_datetime,entry_type)
        if past_doc:
            future_docs = get_future_records(employee,posting_datetime,entry_type)
            if future_docs:
                check_cancel_possible(future_docs,d.amount)
                make_cancel_future_update(future_docs, d.amount)
                d.is_cancelled = True
            else:
                if past_doc.running_balance >= 0:
                    d.is_cancelled = True
        else:
            future_docs = get_future_records(employee,posting_datetime,entry_type)
            if future_docs:
                check_cancel_possible(future_docs,d.amount)
                make_cancel_future_update(future_docs, d.amount)
                d.is_cancelled = True               
            else:
                d.is_cancelled = True
        d.save()
        
def check_cancel_possible(future_docs,amount):
    for doc in future_docs:
        if flt(doc.running_balance) - flt(amount) >= 0:
            continue
        else:
            frappe.throw("It can't be cancelled, it affects the ledger")


def make_cancel_future_update(future_docs,amount):
    for docs in future_docs:
        update_doc = frappe.get_doc("Essdee Advance Ledger Entry",docs.name)
        update_doc.running_balance = flt(update_doc.running_balance) - flt(amount)
        update_doc.save() 
