import { createWebHistory, createRouter } from "vue-router";

import HomeView from "../views/HomeView.vue";
import AboutView from "../views/AboutView.vue";
import DashboardView from "../views/DashboardView.vue";
import KnowledgeBasesView from "../views/KnowledgeBasesView.vue";
import LoginView from "../views/LoginView.vue";
import KnowledgeBaseCreateView from "../views/KnowledgeBaseCreateView.vue";
import KnowledgeBaseDocumentsView from "../views/KnowledgeBaseDocumentsView.vue";
import KnowledgeBaseUploadView from "../views/KnowledgeBaseUploadView.vue";
import ChatView from "../views/ChatView.vue";
import { useUserStore } from "../stores/user";

const routes = [
  { path: "/", component: HomeView },
  { path: "/about", component: AboutView },
  { path: "/login", component: LoginView },
  {
    path: "/dashboard",
    component: DashboardView,
    meta: { requiresAuth: true },
  },
  {
    path: "/knowledge-bases",
    component: KnowledgeBasesView,
    meta: { requiresAuth: true },
  },
  {
    path: "/knowledge-bases/create",
    component: KnowledgeBaseCreateView,
    meta: { requiresAuth: true },
  },
  {
    path: "/knowledge-bases/:id/documents",
    component: KnowledgeBaseDocumentsView,
    meta: { requiresAuth: true },
  },
  {
    path: "/knowledge-bases/:id/upload",
    component: KnowledgeBaseUploadView,
    meta: { requiresAuth: true },
  },
  {
    path: "/knowledge-bases/:id/chat",
    component: ChatView,
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// 路由守卫
router.beforeEach((to) => {
  const userStore = useUserStore();

  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    return "/login";
  }

  if (to.path === "/login" && userStore.isLoggedIn) {
    return "/dashboard";
  }

  return true;
});

export default router;
