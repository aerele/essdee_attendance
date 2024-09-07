<template>
	<ion-page>
		<ion-content :fullscreen="true">
			<FormView
				v-if="formFields.data"
				doctype="Essdee Permission Application"
				v-model="essdeePermissionApplication"
				:isSubmittable="true"
				:fields="formFields.data"
				:id="props.id"
				:showAttachmentView="true"
				@validateForm="validateForm"
			/>
		</ion-content>
	</ion-page>
</template>

<script setup>
import { IonPage, IonContent } from "@ionic/vue"
import { createResource } from "frappe-ui"
import { ref, watch, inject } from "vue"

import FormView from "@/components/FormView.vue"

const dayjs = inject("$dayjs")
const employee = inject("$employee")
const today = dayjs().format("YYYY-MM-DD")

const props = defineProps({
	id: {
		type: String,
		required: false,
	},
})

// reactive object to store form data
const essdeePermissionApplication = ref({})

// get form fields
const formFields = createResource({
	url: "hrms.api.get_doctype_fields",
	params: { doctype: "Essdee Permission Application" },
	transform(data) {
		let fields = getFilteredFields(data)
		console.log(fields)
		return fields.map((field) => {
			if (field.fieldname === "posting_date") field.default = today
			return field
		})
	},
	onSuccess(_data) {
		permissionApprovalDetails.reload()
	},
})
formFields.reload()

let field_list = {}
let hide_fields = ['end_time','end_date']

const permissionApprovalDetails = createResource({
	url: "essdee_attendance.api.get_permission_approval_details",
	params: { employee: employee.data.name },
	onSuccess(data) {
		setPermissionApprovers(data)
	},
})

// form scripts
watch(
	() => essdeePermissionApplication.value.employee,
	(employee_id) => {
		if (props.id && employee_id !== employee.data.name) {
			setFormReadOnly()
		}
	}
)

watch(
	() => [essdeePermissionApplication.value.permission_type, essdeePermissionApplication.value],
	([permission_type, essdeePermissionApplication]) => {
		if(permission_type == 'Personal Permission' && essdeePermissionApplication.docstatus != 0){
			for(let i = 0; i< hide_fields.length ; i++){
				for(let j = 0 ; j < formFields.data.length ; j++){
					if(hide_fields.includes(formFields.data[j]['fieldname'])){
						let temp = formFields.data
						if(j == formFields.data.length - 1){
							formFields.data = temp.slice(0,formFields.data.length - 1)
						}
						else{
							formFields.data = temp.slice(0,j).concat(temp.slice(j+1,formFields.data.length))
						}
					}
				}
			}
		}
		else{
			formFields.reload()
		}
	}
)

watch(
	() => [essdeePermissionApplication.value.start_time,essdeePermissionApplication.value.end_time],
	([start_time, end_time]) => {
		validateDates(start_time, end_time)
	}
)

// helper functions
function getFilteredFields(fields) {
	// reduce noise from the form view by excluding unnecessary fields
	// ex: employee and other details can be fetched from the session user
	const excludeFields = [
		"naming_series",
		"sb_other_details",
		"salary_slip",
		"letter_head",
		'department',
		'designation'
	]

	const employeeFields = [
		"employee",
		"employee_name",
		"company",
		"status",
		"posting_date",
	]

	if (!props.id) excludeFields.push(...employeeFields)
	return fields.filter((field) => !excludeFields.includes(field.fieldname))
}
let start_time_st = null
let end_time_ed = null
function setFormReadOnly() {
	if (essdeePermissionApplication.value.permission_approver === employee.data.user_id) return
	formFields.data.map((field) => (field.read_only = true))
}

function validateDates(start_time, end_time) {
	if(start_time){
		if(typeof(start_time) == 'string'){
			start_time_st = start_time
		}
		else{
			start_time_st = start_time.target.value
		}
	}
	if(end_time){
		if(typeof(end_time) == 'string'){
			end_time_ed = end_time
		}
		else{
			end_time_ed = end_time.target.value
		}
	}
}

function setPermissionApprovers(data) {
	const permission_approver = formFields.data?.find(
		(field) => field.fieldname === "permission_approver"
	)
	permission_approver.reqd = data?.is_mandatory
	permission_approver.documentList = data?.department_approvers.map((approver) => ({
		label: approver.full_name
			? `${approver.name} : ${approver.full_name}`
			: approver.name,
		value: approver.name,
	}))
	essdeePermissionApplication.value.permission_approver = data?.permission_approver
}

function areValuesSet() {
	return (
		essdeePermissionApplication.value.start_date &&
		essdeePermissionApplication.value.end_date &&
		essdeePermissionApplication.value.permission_type
	)
}

function validateForm() {
	if(start_time_st && start_time_st.length < 7){
		start_time_st = start_time_st + ":00"
	}
	if(end_time_ed && end_time_ed.length < 7){
		end_time_ed = end_time_ed + ":00"
	}
	essdeePermissionApplication.value.employee = employee.data.name
	essdeePermissionApplication.value.start_time = start_time_st
	essdeePermissionApplication.value.end_time = end_time_ed
}
</script>
