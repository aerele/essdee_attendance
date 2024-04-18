# Copyright (c) 2024, Aerele and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class EmployeeIDCard(Document):
	pass

# def get_qr_code_base64_str(content, scale=1):
# 	from pyqrcode import create as qrcreate
# 	qr = qrcreate(content)
# 	qr_str = qr.png_as_base64_str(scale=scale)
# 	return qr_str