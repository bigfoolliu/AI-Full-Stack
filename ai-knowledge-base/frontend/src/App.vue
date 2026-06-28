<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const navItems = [
  { label: '工作台', to: '/dashboard' },
  { label: '知识库', to: '/knowledge-bases' },
]

const pageTitleMap: Record<string, string> = {
  '/dashboard': '工作台',
  '/knowledge-bases': '知识库',
}

const currentTitle = computed(() => pageTitleMap[route.path] ?? 'AI 知识库')
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
          <span class="shell-user__avatar">L</span>
          <div>
            <strong>刘同学</strong>
            <p>后端转 AI 全栈</p>
          </div>
        </div>
      </header>

      <main class="shell-content">
        <RouterView />
      </main>
    </div>
  </div>
</template>
