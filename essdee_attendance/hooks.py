# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "essdee_attendance"
app_title = "Essdee Attendance"
app_publisher = "Aerele"
app_description = "Frappe application to track attendance"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "admin@aerele.in"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/essdee_attendance/css/essdee_attendance.css"
# app_include_js = "/assets/essdee_attendance/js/essdee_attendance.js"

# include js, css files in header of web template
# web_include_css = "/assets/essdee_attendance/css/essdee_attendance.css"
# web_include_js = "/assets/essdee_attendance/js/essdee_attendance.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "essdee_attendance/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "essdee_attendance.install.before_install"
# after_install = "essdee_attendance.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "essdee_attendance.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
# 	"all": [
# 		"essdee_attendance.tasks.all"
# 	],
	"daily": [
		"essdee_attendance.essdee_attendance.doctype.essdee_attendance_settings.essdee_attendance_settings.submit_all_record"
	],
	"hourly": [
		"essdee_attendance.essdee_attendance.doctype.essdee_attendance_settings.essdee_attendance_settings.mark_attendance"
	],
# 	"weekly": [
# 		"essdee_attendance.tasks.weekly"
# 	]
# 	"monthly": [
# 		"essdee_attendance.tasks.monthly"
# 	]
}

# Testing
# -------

# before_tests = "essdee_attendance.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "essdee_attendance.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "essdee_attendance.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]
after_install = "essdee_attendance.essdee_attendance.doctype.essdee_attendance_settings.essdee_attendance_settings.make_custom_field"
