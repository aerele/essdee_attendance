<template>
	<div class="flex flex-col w-full">
		<div class="flex flex-row justify-between items-center px-4">
			<div class="text-md text-gray-800 font-bold">Permission Balance:  {{permissionBalance.data}} </div>
			
			<router-link
				:to="{ name: 'EssdeePermissionApplicationListView' }"
				v-slot="{ navigate }"
			>
				<div
					@click="navigate"
					class="text-sm text-gray-800 font-semibold cursor-pointer underline underline-offset-2"
				>
					View Permission History
				</div>
			</router-link>
		</div>

		<!-- Leave Balance Dashboard -->
		<!-- <div
			class="flex flex-row gap-4 overflow-x-auto py-2 mt-3"
			v-if="permissionBalance.data"
		>
			<div
				v-for="(allocation, permission_type, index) in permissionBalance.data"
				:key="permission_type"
				class="flex flex-col bg-white border-none rounded-lg drop-shadow-md gap-2 p-4 items-start first:ml-4"
			>
				<SemicircleChart
					:percentage="33"
					:colorClass="getChartColor(index)"
				/>
				<div class="text-gray-800 font-bold text-base">
					{{ `${1}/${5}` }}
				</div>
				<div class="text-gray-600 font-normal text-sm w-24 leading-4">
					{{ `${permission_type} balance` }}
				</div>
			</div>
		</div>

		<EmptyState message="You have no leaves allocated" v-else /> -->
	</div>
</template>

<script setup>
// import SemicircleChart from "@/components/SemicircleChart.vue"

import { permissionBalance } from "@/data/permissions"

// const getChartColor = (index) => {
	// note: tw colors - rose-400, pink-400 & purple-500 of the old frappeui palette #918ef5
	// const chartColors = ["text-[#fb7185]", "text-[#f472b6]", "text-[#918ef5]"]
	// return chartColors[index % chartColors.length]

</script>
