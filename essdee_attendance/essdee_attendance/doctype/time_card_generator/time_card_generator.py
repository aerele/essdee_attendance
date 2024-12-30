# Copyright (c) 2024, Aerele and contributors
# For license information, please see license.txt

import random
import datetime
import frappe, json
from datetime import datetime as date_time
from frappe.model.document import Document
from frappe.utils import add_to_date, getdate, get_last_day, flt, time_diff_in_hours
from frappe.utils.xlsxutils import read_xls_file_from_attached_file, read_xlsx_file_from_attached_file

class TimeCardGenerator(Document):
	pass

@frappe.whitelist()
def create_time_card_timing(import_file):
	doc = frappe.get_single("Time Card Generator")
	time_list = frappe.get_list("Time Card Timing", filters={"month":doc.month,"year":doc.year,"worker_type":doc.type})
	if len(time_list) > 0:
		frappe.throw(f"Time List Created for {doc.month} {doc.year}")

	month_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
	if not import_file:
		frappe.throw("No file provided!")

	file_doc = frappe.get_doc("File", {"file_url": import_file})
	if not file_doc:
		frappe.throw("File not found!")

	if len(doc.time_card_generator_details) == 0:
		frappe.throw("Enter the Time Card Generator Shift Details")

	raw_data = get_data_from_template_file(file_doc)
	header = raw_data[0]
	raw_data = raw_data[1:]
	
	shifts = {}
	shift_prob = {}
	for shift in doc.time_card_generator_details:
		if shift_prob.get(shift.shift_hours):
			shift_prob[shift.shift_hours].append(shift.probability)
		else:
			shift_prob[shift.shift_hours] = [shift.probability]	
		
		if shifts.get(shift.shift_hours):
			shifts[shift.shift_hours][shift.probability] = [shift.in_time, shift.out_time, shift.break_hours]
		else:
			shifts[shift.shift_hours] = {}
			shifts[shift.shift_hours][shift.probability] = [shift.in_time, shift.out_time, shift.break_hours]

	month_index = month_list.index(doc.month) + 1
	month_start_date = str(doc.year) +"-"+str(month_index)+"-"+str(1)
	doc.month_start = month_start_date
	month_start_date = getdate(month_start_date)
	month_end_date = get_last_day(month_start_date)
	doc.month_end = month_end_date
	
	y,m,d = str(month_end_date).split("-")
	last_date = d
	doc_data_list = {}
	now_time = date_time.now()
	for row in raw_data:
		employee_name = None
		for idx, d in enumerate(row):
			if idx != 0 and header[idx] not in ["S.No","Employee Name"]:
				if header[idx] == "Employee":
					if doc_data_list.get(header[idx]):
						frappe.throw("Duplicate Employees are in the list")
					else:
						doc_data_list[d] = {}
					employee_name = d
				else:
					if int(header[idx]) > int(last_date):
						break
					cur_date = str(doc.year)+"-"+str(month_index)+"-"+str(header[idx])
					cur_date = getdate(cur_date)

					if d not in ['WO',"A","NH","EL","FH","NA","OH", "CL", None, "None"] and flt(d) > flt(0): 
						s = random.choices(shift_prob[d], shift_prob[d], k=1)
						in_time, out_time, break_hour = shifts[d][s[0]]
						in_random = random.randint(doc.in_time_start_range, doc.in_time_end_range)
						out_random = random.randint(doc.out_time_start_range, doc.out_time_end_range)
						in_time = now_time + add_to_date(in_time, minutes = in_random) - now_time
						out_time = now_time + add_to_date(out_time, minutes = out_random) - now_time

						diff = time_diff_in_hours(out_time, in_time) - break_hour
						x = time_to_hours(diff)
						doc_data_list[employee_name][cur_date] = {
							"in_time": get_norm_time(in_time),
							"out_time": get_norm_time(out_time),
							"shift_hours": d,
							"present": "P",
							"working_hour_time": str(x[0])+":"+str(x[1]),
							"working_hours": diff,
						}
					else:
						if d == 0 or d == '0':
							d = 'A'
						doc_data_list[employee_name][cur_date] = {
							"in_time": None,
							"out_time": None,
							"shift_hours": None,
							"present": d,
							"working_hour_time":None,
							"working_hours": None,
						}

	for employee_id, employee_data in doc_data_list.items():
		for date, timing in employee_data.items():
			new_doc = frappe.new_doc("Time Card Timing")
			new_doc.employee = employee_id
			new_doc.in_time = timing['in_time']
			new_doc.out_time = timing['out_time']
			new_doc.shifts = timing['shift_hours']
			new_doc.working_hours = timing['working_hour_time']
			if timing['shift_hours'] and timing['shift_hours'] > 1:
				new_doc.ot_shift = 1
				ot_hours = timing['working_hours'] - 8
				new_doc.ot_hours = ot_hours
				x = time_to_hours(ot_hours)
				new_doc.ot_working_hours = str(x[0])+":"+str(x[1])
			y,m,d = str(date).split("-")
			new_doc.date = d+"-"+m+"-"+y
			new_doc.month = doc.month
			new_doc.year = doc.year
			new_doc.status = timing['present']
			new_doc.worker_type = doc.type
			new_doc.save()	

@frappe.whitelist()
def update_time_card_timing(import_file):
	if not import_file:
		frappe.throw("No file provided!")

	file_doc = frappe.get_doc("File", {"file_url": import_file})
	if not file_doc:
		frappe.throw("File not found!")
	doc = frappe.get_single("Time Card Generator")
	time_list = frappe.get_list("Time Card Timing", filters={"month":doc.month,"year":doc.year,"worker_type":doc.type})
	if len(time_list) == 0:
		frappe.throw(f"Time List Not Created for {doc.month} {doc.year}")
	else:
		frappe.db.sql(
			f"""
				delete from `tabTime Card Timing` WHERE month = '{doc.month}' AND year = '{doc.year}' AND worker_type = '{doc.type}' 
			"""
		)

	create_time_card_timing(import_file)	

def get_norm_time(time):
	hour, min, sec = str(time).split(":")
	x = "AM"
	if int(hour) >= 13:
		hour = int(hour) - 12
		x = "PM"
	return str(hour) + ":" + str(min) + " " + str(x)	

def get_data_from_template_file(file_doc):
	parts = file_doc.get_extension()
	extension = parts[1]
	content = file_doc.get_content()
	extension = extension.lstrip(".")

	if extension not in ("xlsx", "xls"):
		frappe.throw("Import template should be type of .xlsx or .xls")

	if content:
		data = None
		if extension == "xlsx":
			data = read_xlsx_file_from_attached_file(fcontent=content)
		elif extension == "xls":
			data = read_xls_file_from_attached_file(content)
		return data	

@frappe.whitelist()
def get_time_card_datas():
	month_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
	doc = frappe.get_single("Time Card Generator")
	month_index = month_list.index(doc.month) + 1
	month_start_date = str(doc.year) +"-"+str(month_index)+"-"+str(1)
	month_start_date = getdate(month_start_date)
	y,m,d = str(month_start_date).split("-")
	doc.month_start = d+"-"+m+"-"+y
	month_end_date = get_last_day(month_start_date)
	y,m,d = str(month_end_date).split("-")
	doc.month_end = d+"-"+m+"-"+y
	url = doc.get_url()
	emt, app, app_name, encrypt = url.split("/")
	app_name = "print"
	url = "/"+app+"/"+app_name+"/"+encrypt
	employees = frappe.db.sql(
		f"""
			Select employee from `tabTime Card Timing` WHERE month = '{doc.month}' AND year = '{doc.year}' AND worker_type = '{doc.type}' GROUP BY employee
		""", as_list=True
	)
	if len(employees) == 0:
		frappe.throw(f"No Data for {doc.month} {doc.year}")
	attendance_data = {}
	for employee in employees:
		department, designation, full_name = frappe.get_value("Employee",employee[0],['department','designation','employee_name'])
		start_time = get_norm_time(doc.shift_start_time)
		end_time = get_norm_time(doc.shift_end_time)
		res = frappe.db.sql(
			f"""
				Select employee, in_time, out_time, shift_hours, ot_hours, date, working_hours, status,shifts, ot_shift, ot_working_hours, ot_hours 
				from `tabTime Card Timing` WHERE month = '{doc.month}' AND year = '{doc.year}' and employee='{employee[0]}' ORDER BY date ASC
			""", as_dict=True
		)
		attendance_data[employee[0]] = {}
		attendance_data[employee[0]]['attendance'] = res
		attendance_data[employee[0]]["department"] = department
		attendance_data[employee[0]]["designation"] = designation
		attendance_data[employee[0]]["name"] = full_name
		attendance_data[employee[0]]['start_time'] = start_time
		attendance_data[employee[0]]['end_time'] = end_time
	
	doc.print_details_json = attendance_data
	doc.save()
	return url

@frappe.whitelist()
def time_to_hours(diff):
	x = str(datetime.timedelta(hours=diff))
	x = x.split(".")
	x = x[0].split(":")
	return x

@frappe.whitelist()
def get_dict_object(data):
	return json.loads(data)
