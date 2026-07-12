<script setup lang="ts">
import { computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useUserStore } from './stores/user';
interface BreadcrumbItem {
  label: string;
  to?: string;
}

const router = useRouter();
const route = useRoute();
const userStore = useUserStore();

const navItems = [
  { label: '工作台', to: '/dashboard' },
  { label: '知识库', to: '/knowledge-bases' },
];

const breadcrumbItems = computed((): BreadcrumbItem[] => {
  const path = route.path;
  if (path === '/dashboard') return [{ label: '工作台' }];
  if (path === '/knowledge-bases') return [{ label: '知识库管理' }];
  if (path === '/knowledge-bases/create')
    return [{ label: '知识库管理', to: '/knowledge-bases' }, { label: '新建知识库' }];
  if (path.startsWith('/knowledge-bases/') && path.endsWith('/documents'))
    return [{ label: '知识库管理', to: '/knowledge-bases' }, { label: '文档列表' }];
  if (path.startsWith('/knowledge-bases/') && path.endsWith('/upload'))
    return [{ label: '知识库管理', to: '/knowledge-bases' }, { label: '上传文档' }];
  return [{ label: 'AI 知识库' }];
});

const pageTitleMap: Record<string, string> = {
  '/dashboard': '工作台',
  '/knowledge-bases': '知识库',
};

const currentTitle = computed(() => pageTitleMap[route.path] ?? 'AI 知识库');
const displayUsername = computed(() => userStore.nickname || userStore.username || '未登录用户');
const displayRole = computed(() => (userStore.isLoggedIn ? '已登录' : '点击登录'));

const handleLogout = () => {
  userStore.logout();
  router.push('/login');
};
</script>

<template>
  <div class="app-shell">
    <aside class="shell-sidebar">
      <div class="shell-brand">
        <span class="shell-brand__eyebrow">AI Full Stack</span>
        <strong>AI 知识库</strong>
      </div>

      <nav class="shell-nav" aria-label="主导航">
        <RouterLink v-for="item in navItems" :key="item.to" :to="item.to" class="shell-nav__link">
          {{ item.label }}
        </RouterLink>
      </nav>
    </aside>

    <div class="shell-workspace">
      <header class="shell-topbar">
        <div>
          <el-breadcrumb>
            <el-breadcrumb-item v-for="item in breadcrumbItems" :key="item.label" :to="item.to">
              {{ item.label }}
            </el-breadcrumb-item>
          </el-breadcrumb>
          <h1>{{ currentTitle }}</h1>
        </div>
        <div class="shell-user">
          <RouterLink to="/login" class="shell-user__profile">
            <span class="shell-user__avatar">{{ displayUsername.slice(0, 1).toUpperCase() }}</span>
            <div>
              <strong>{{ displayUsername }}</strong>
              <p>{{ displayRole }}</p>
            </div>
          </RouterLink>
          <button
            v-if="userStore.isLoggedIn"
            type="button"
            class="shell-user__logout"
            @click="handleLogout"
          >
            退出
          </button>
        </div>
      </header>

      <main class="shell-content">
        <RouterView />
      </main>
    </div>
  </div>
</template>
