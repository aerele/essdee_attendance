<template>
	<ion-page>
		<PermissionListView
			doctype="Essdee Permission Application"
			pageTitle="Permission History"
			:tabButtons="TAB_BUTTONS"
			:fields="PERMISSION_FIELDS"
			:filterConfig="FILTER_CONFIG"
		/>
	</ion-page>
</template>

<script setup>
import { IonPage } from "@ionic/vue"
import PermissionListView from "@/components/PermissionListView.vue"

const TAB_BUTTONS = ["My Permission", "Team Permission"]
const PERMISSION_FIELDS = [
	"name",
	"employee",
	"employee_name",
	// "department",
	// "designation",
	"permission_type",
	"start_date",
	"end_date",
	"start_time",
	"end_time",
	"status",
]
const STATUS_FILTER_OPTIONS = ["Open", "Approved", "Rejected"]
const FILTER_CONFIG = [
	{
		fieldname: "status",
		fieldtype: "Select",
		label: "Status",
		options: STATUS_FILTER_OPTIONS,
	},
	{
		fieldname: "permission_type",
		fieldtype: "Select",
		label: "Permission Type",
		options: "/nPersonal Permission/nOn Duty",
	},
	{
		fieldname: "employee",
		fieldtype: "Link",
		label: "Employee",
		options: "Employee",
	},
	// {
	// 	fieldname: "department",
	// 	fieldtype: "Link",
	// 	label: "Department",
	// 	options: "Department",
	// },
	{ fieldname: "start_date", fieldtype: "Date", label: "Start Date" },
	{ fieldname: "end_date", fieldtype: "Date", label: "End Date" },
	{ fieldname: "start_time", fieldtype: "Time", label: "Start Time" },
	{ fieldname: "end_time", fieldtype: "Time", label: "End Time" },
]
</script>
