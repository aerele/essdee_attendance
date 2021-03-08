# -*- coding: utf-8 -*-
# Copyright (c) 2021, Aerele and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from essdee_attendance.essdee_attendance.doctype.essdee_attendance_settings.essdee_attendance_settings import sync_device
from zk import ZK
from zk.finger import Finger
from zk.user import User

class EssdeeBiometricDeviceSyncLog(Document):
	pass

def process_unsync_record():
	# Called every 30 minutes via hooks
	unsynced_doc_list = frappe.db.get_all('Essdee Biometric Device Sync Log',{'status':['in', ['Queued','Error']], 'resend_count': ['<', 5]},['name', 'device_ip'])
	ip_list = frappe.db.get_all('Essdee Biometric Device', ['ip'])
	final_list = []
	for ip in ip_list:
		doc_list = []
		for doc in unsynced_doc_list:
			if ip['ip'] == doc['device_ip']:
				doc_list.append(doc['name'])
		if doc_list:
			final_list.append({'ip':ip['ip'], 'doc_list': doc_list})

	if final_list:
		for val in final_list:
			conn = None
			try:
				conn = sync_device(val['ip'])
				if conn:
					conn.disable_device()
					for doc_name in val['doc_list']:
						doc = frappe.get_doc('Essdee Biometric Device Sync Log', doc_name)
						try:
							employee = frappe.get_doc('Employee', doc.employee)
							if doc.status == 'Error':
								doc.resend_count += 1
							if doc.action == 'Delete':
								conn.delete_user(uid= int(employee.attendance_device_id))
							if doc.action == 'Update':
								conn.set_user(uid= int(employee.attendance_device_id), name= employee.employee_name, user_id= employee.attendance_device_id)
							if doc.action == 'Sync Templates' or doc.action == 'All':
								templates = []
								for row in employee.finger_print_details:
									templates.append(Finger.json_unpack(json_unpack(row, int(employee.attendance_device_id))))
								if templates:
									zk_user = User(int(employee.attendance_device_id), employee.employee_name,0,user_id = employee.attendance_device_id)
									conn.save_user_template(zk_user,templates)
							doc.status = 'Completed'
						except:
							doc.status = 'Error'
							doc.error_message = frappe.get_traceback()
						doc.save()
			except:
				frappe.log_error(frappe.get_traceback())
			finally:
				if conn:
					conn.refresh_data()
					conn.enable_device()
					conn.disconnect()

def json_unpack(row, uid):
	return {
		"uid": uid,
		"fid":int(row.id[-1]),
		"template":row.template,
		"valid": True
	}