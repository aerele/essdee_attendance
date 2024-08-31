<template>
	<BaseLayout pageTitle="Permissions">
		<template #body>
			<div class="flex flex-col items-center mt-7 mb-7 py-4">
				<PermissionBalance />

				<div class="flex flex-col gap-7 mt-5 px-4 w-full">
					<router-link
						:to="{ name: 'EssdeePermissionApplicationFormView' }"
						v-slot="{ navigate }"
					>
						<Button
							@click="navigate"
							variant="solid"
							class="py-5 text-base w-full"
						>
							Request a Permission
						</Button>
					</router-link>
					<div>
						<div class="text-lg text-gray-800 font-bold">Recent Permissions</div>
						<PermissionRequestList
							:component="markRaw(PermissionRequestItem)"
							:items="myPermissions.data"
							:addListButton="true"
							listButtonRoute="EssdeePermissionApplicationListView"
						/>
					</div>
				</div>
			</div>
		</template>
	</BaseLayout>
</template>

<script setup>
import { markRaw } from "vue"

import BaseLayout from "@/components/BaseLayout.vue"
import PermissionBalance from "@/components/PermissionBalance.vue"
import PermissionRequestList from "@/components/PermissionRequestList.vue"
import PermissionRequestItem from "@/components/PermissionRequestItem.vue"
// import Holidays from "@/components/Holidays.vue"

import { myPermissions } from "@/data/permissions"
</script>
