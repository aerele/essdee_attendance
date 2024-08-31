const routes = [
	{
		name: "EssdeePermissionApplicationListView",
		path: "/permission-applications",
		component: () => import("@/views/permission/List.vue"),
	},
	{
		name: "EssdeePermissionApplicationFormView",
		path: "/permission-applications/new",
		component: () => import("@/views/permission/Form.vue"),
	},
	{
		name: "EssdeePermissionApplicationDetailView",
		path: "/permission-applications/:id",
		props: true,
		component: () => import("@/views/permission/Form.vue"),
	},
]

export default routes
