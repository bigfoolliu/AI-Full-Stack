<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'

const router = useRouter()
const userStore = useUserStore()
const username = ref('')
const password = ref('')

const handleLogin = async () => {
  const trimmedUsername = username.value.trim()
  const trimmedPassword = password.value.trim()

  userStore.clearError()

  if (!trimmedUsername || !trimmedPassword) {
    return
  }

  const success = await userStore.login(trimmedUsername, trimmedPassword)

  if (success) {
    router.push('/dashboard')
  }
}
</script>

<template>
  <section class="login-page">
    <div class="login-card">
      <div class="login-card__header">
        <p class="login-card__eyebrow">Welcome Back</p>
        <h1>登录 AI 知识库</h1>
        <p class="login-card__description">
          输入后端 mock 账号密码，完成第一次真实前后端联调。
        </p>
      </div>

      <form class="login-form" @submit.prevent="handleLogin">
        <label class="login-field">
          <span>用户名</span>
          <input id="username" v-model="username" type="text" placeholder="请输入用户名" autocomplete="username" />
        </label>

        <label class="login-field">
          <span>密码</span>
          <input id="password" v-model="password" type="password" placeholder="请输入密码" autocomplete="current-password" />
        </label>

        <button type="submit" class="login-submit" :disabled="userStore.loginLoading">
          {{ userStore.loginLoading ? '登录中...' : '登录' }}
        </button>
      </form>

      <p v-if="userStore.loginError" class="login-card__error">{{ userStore.loginError }}</p>

      <p class="login-card__hint">
        当前 mock 账号：`admin`，密码：`123456`
      </p>
    </div>
  </section>
</template>
