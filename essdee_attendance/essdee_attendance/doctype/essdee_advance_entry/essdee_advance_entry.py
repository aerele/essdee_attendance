# Copyright (c) 2024, Aerele and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from essdee_attendance.essdee_attendance.advance_ledger import make_ledger
from essdee_attendance.essdee_attendance.advance_ledger import cancel_ledger
from erpnext.stock.utils import get_combine_datetime
import openpyxl
from datetime import datetime
from io import BytesIO

class EssdeeAdvanceEntry(Document):
	def validate(self):
		self.posting_datetime = get_combine_datetime(self.posting_date, self.posting_time)
	
	def on_submit(self):
		details = get_list(self)
		make_ledger(details)
	def on_cancel(self):
		cancel_ledger(self.name,'Essdee Advance Entry')	


def get_list(doc):
	x = []
	for row in doc.essdee_advance_entry_details:
		dic = {
			"employee" : row.employee,
			"posting_date" : doc.posting_date,
			"posting_time" : doc.posting_time,
			"posting_datetime": doc.posting_datetime,
			"amount": row.amount,
			"type":row.type,
			"doctype" : "Essdee Advance Entry",
			"docname" : doc.name
		}
		x.append(dic)		
	return x	

@frappe.whitelist()
def download_entries(**args):
	doc_name = args['doc_name']
	columns = ['Employee','Employee Name','Amount', "Type",'Bank Account Status','Salary Mode', 'Advance Slip',"Date"]

	entries = []
	doc = frappe.get_doc('Essdee Advance Entry',doc_name)
	for row in doc.essdee_advance_entry_details:
		emp_name, bank_status = frappe.get_value("Employee", row.employee, ['employee_name', "sd_bank_account_status"])
		entries.append([row.employee, emp_name, str(row.amount), row.type, bank_status, row.salary_mode, doc_name, str(doc.posting_date)])
	
	doc.downloaded_time = datetime.now()
	doc.save()
	wb = openpyxl.Workbook(write_only=True)
	ws = wb.create_sheet("Sheet1", 0)
	ws.append(columns)
	for entry in entries:
		ws.append(entry)  
	 
	xlsx_file = BytesIO()
	wb.save(xlsx_file)

	frappe.response["filename"] = doc_name + ".xlsx"
	frappe.response["filecontent"] = xlsx_file.getvalue()
	frappe.response["type"] = "binary"