<template>
	<div class="w-full">
		<div class="text-lg font-medium text-gray-900 pb-4">{{ 'Permission Requests' }}</div>
		<TabButtons
			:buttons="[{ label: 'My Requests' }, { label: 'Team Requests' }]"
			v-model="activeTab"
		/>
		<PermissionRequestList v-if="activeTab == 'My Requests'" :items="myRequests" />
		<PermissionRequestList
			v-else-if="activeTab == 'Team Requests'"
			:items="teamRequests"
			:teamRequests="true"
		/>
	</div>
</template>

<script setup>
import { ref, inject, onMounted, computed, markRaw } from "vue"

import TabButtons from "@/components/TabButtons.vue"
import PermissionRequestList from "@/components/PermissionRequestList.vue"

import { myPermissions, teamPermissions } from "@/data/permissions"
import { myClaims, teamClaims } from "@/data/claims"

import PermissionRequestItem from "@/components/PermissionRequestItem.vue"
import ExpenseClaimItem from "@/components/ExpenseClaimItem.vue"

import { useListUpdate } from "@/composables/realtime"

const activeTab = ref("My Requests")
const socket = inject("$socket")

const myRequests = computed(() => updateRequestDetails(myPermissions, myClaims))

const teamRequests = computed(() =>
	updateRequestDetails(teamPermissions, teamClaims)
)

function updateRequestDetails(leaves, claims) {

	const requests = [...(leaves.data || []), ...(claims.data || [])]
	requests.forEach((request) => {
		if (request.doctype === "Essdee Permission Application") {
			request.component = markRaw(PermissionRequestItem)
		} else if (request.doctype === "Expense Claim") {
			request.component = markRaw(ExpenseClaimItem)
		}
	})
	return getSortedRequests(requests)
}

function getSortedRequests(list) {
	// return top 10 requests sorted by posting date
	return list
		.sort((a, b) => {
			return new Date(b.posting_date) - new Date(a.posting_date)
		})
		.splice(0, 10)
}

onMounted(() => {
	useListUpdate(socket, "Essdee Permission Application", () => teamPermissions.reload())
	useListUpdate(socket, "Expense Claim", () => teamClaims.reload())
})
</script>
