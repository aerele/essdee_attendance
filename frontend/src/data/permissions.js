import { createResource } from "frappe-ui"
import { employeeResource } from "./employee"

import dayjs from "@/utils/dayjs"

const transformPermissionData = (data) => {
	return data.map((permission) => {
		permission.leave_dates = getPermissions(permission)
		permission.doctype = "Essdee Permission Application"
		return permission
	})
}

export const getPermissions = (permission) => {
	return `${dayjs(permission.start_date).format("D MMM")} ${permission.start_time}- ${dayjs(permission.end_date).format("D MMM")} ${permission.end_time}`
}

export const myPermissions = createResource({
	url: "essdee_attendance.api.get_permission_applications",
	params: {
		employee: employeeResource.data.name,
		limit: 10,
	},
	auto: true,
	cache: "essdee_attendance:my_permissions",
	transform(data) {
		return transformPermissionData(data)
	},
})

export const teamPermissions = createResource({
	url: "essdee_attendance.api.get_permission_applications",
	params: {
		employee: employeeResource.data.name,
		approver_id: employeeResource.data.user_id,
		for_approval: true,
		limit: 10,
	},
	auto: true,
	cache: "essdee_attendance:team_permissions",
	transform(data) {
		return transformPermissionData(data)
	},
})

export const permissionBalance = createResource({
	url: "essdee_attendance.api.get_personal_permission_balance",
	params: {
		employee: employeeResource.data.name,
	},
	auto: true,
	cache: "essdee_attendance:permission_balance",
	transform: (data) => {
		return data
	},
})
