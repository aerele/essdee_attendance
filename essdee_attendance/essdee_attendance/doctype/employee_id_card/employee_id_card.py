# Copyright (c) 2024, Aerele and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EmployeeIDCard(Document):
	pass

def generate_qr_code(qr_text, scale=5):
    import pyqrcode
    d = pyqrcode.create(qr_text).png_as_base64_str(scale=scale, quiet_zone=1)
    return f'<img src="data:image/png;base64,{d}">'

def generate_barcode(data):
    from io import BytesIO
    from barcode import Code128
    from barcode.writer import ImageWriter
    import base64
  
    stream = BytesIO()
    Code128(str(data), writer=ImageWriter()).write(
        stream,
        {
            "module_width": 0.5,
            "module_height": 18.0,
            "text_distance": 10,
            "foreground": "black",
            "quiet_zone": 10.5,
        	"write_text": True,
            "font_size":20,
        },
    )
    barcode_base64 = base64.b64encode(stream.getbuffer()).decode()
    stream.close()

    return f'<img src="data:image/png;base64,{barcode_base64}">'

def get_numbers_from_last(data):
    length = len(data)
    index = length
    for i in range(length-1, -1, -1):
        try:
            j = int(data[i])
            index = i
        except:
            break
    return data[index:]