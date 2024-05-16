import frappe
from frappe.utils import flt

def create_advance_ledger_entry(data,running_balance):
    new_doc = frappe.new_doc('Essdee Advance Ledger Entry')
    new_doc.employee = data['employee']
    new_doc.posting_date = data['posting_date']
    new_doc.posting_time = data['posting_time']
    new_doc.amount = data['amount']
    new_doc.type = data['type']
    new_doc.transaction_type = data['doctype']
    new_doc.transaction_name = data['docname']
    new_doc.running_balance = running_balance
    new_doc.save()

@frappe.whitelist()
def make_ledger(detail_list):
    for row in detail_list:
        check_and_create_ledger(row)               

def check_and_create_ledger(data):
    past_doc = get_last_past_record(data['employee'],data['posting_datetime'],data['type'])
    running_balance = flt(data['amount'])
    if past_doc:
        running_balance += flt(past_doc.running_balance)
        if running_balance < 0:
            show_error(data['type'],data['amount'],data['employee'])
    
    future_docs = get_future_records(data['employee'], data['posting_datetime'], data['type'])

    if running_balance >= 0 and future_docs:
        check_for_future(data,future_docs,data['amount'])
    elif running_balance >= 0:
        create_advance_ledger_entry(data,data['amount'])
    else:
        show_error(data['type'],data['amount'],data['employee']) 

def check_for_future(data,future_docs,running_balance):
    check_is_possible(running_balance,future_docs,data['employee'],data['amount'],data['type'])
    make_future_update(data,running_balance,future_docs)

def show_error(type,amount,employee):
    frappe.throw(f"In {type}, the amount {amount} is not applicable for {employee}")    


def get_last_past_record(employee,posting_datetime, entry_type):
    doc = frappe.db.sql(
        """
        SELECT *
        FROM `tabEssdee Advance Ledger Entry`
        WHERE employee = %s
            AND type = %s
            AND (
                posting_datetime <= %s
            )
            AND is_cancelled = 0
        ORDER BY posting_datetime DESC limit 1""",
        (employee,entry_type,posting_datetime),
        as_dict=True,
    )
    if doc: 
        return doc[0]
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
    return docs

def check_is_possible(running_balance,docs,employee,amount,entry_type):
    x = flt(running_balance)
    for doc in docs:
        s = flt(doc.amount) + flt(x)
        if s < 0:
            frappe.throw(f'In {entry_type}, the amount {amount} is not applicable for {employee}')
        else:
            x = s

def make_future_update(data,running_balance,docs):
    new_entry_running_balance = running_balance
    create_advance_ledger_entry(data,running_balance)
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
        past_doc = get_last_past_record(d.employee,d.posting_datetime,d.type)
        future_docs = get_future_records(d.employee,d.posting_datetime,d.type)
        if future_docs:
            check_cancel_possible(future_docs,d.amount)
            make_cancel_future_update(future_docs,d.amount)
            d.is_cancelled = True
        elif past_doc:
            if past_doc.running_balance >= 0:
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
