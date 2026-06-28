<script setup lang="ts">
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from './stores/user'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const navItems = [
  { label: '工作台', to: '/dashboard' },
  { label: '知识库', to: '/knowledge-bases' },
]

const pageTitleMap: Record<string, string> = {
  '/dashboard': '工作台',
  '/knowledge-bases': '知识库',
}

const currentTitle = computed(() => pageTitleMap[route.path] ?? 'AI 知识库')
const displayUsername = computed(() => userStore.username || '未登录用户')
const displayRole = computed(() => (userStore.isLoggedIn ? '后端转 AI 全栈' : '点击登录'))

// 登出后返回到登陆页
const handleLogout = () => {
  userStore.logout()
  router.push('/login')
}
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
          <p class="shell-topbar__label">控制台</p>
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
          <button v-if="userStore.isLoggedIn" type="button" class="shell-user__logout" @click="handleLogout">
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
