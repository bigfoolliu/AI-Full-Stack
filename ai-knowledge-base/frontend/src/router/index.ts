import { createWebHistory, createRouter } from "vue-router";

import HomeView from "../views/HomeView.vue";
import AboutView from "../views/AboutView.vue";
import DashboardView from "../views/DashboardView.vue";
import KnowledgebasesView from "../views/KnowledgebasesView.vue";
import LoginView from "../views/LoginView.vue";

const routes = [
  { path: "/", component: HomeView },
  { path: "/about", component: AboutView },
  { path: "/login", component: LoginView },
  { path: "/dashboard", component: DashboardView },
  { path: "/knowledge-bases", component: KnowledgebasesView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
