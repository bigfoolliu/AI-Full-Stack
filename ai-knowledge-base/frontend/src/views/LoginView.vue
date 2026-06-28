<script setup lang="ts">
import { ref } from 'vue'

const username = ref('')
const password = ref('')
</script>

<template>
  <section class="login-page">
    <div class="login-card">
      <div class="login-card__header">
        <p class="login-card__eyebrow">Welcome Back</p>
        <h1>登录 AI 知识库</h1>
        <p class="login-card__description">
          这是 Day 2 的静态登录表单版本，先把页面和链路搭起来，后面再接入真实登录逻辑。
        </p>
      </div>

      <form class="login-form" @submit.prevent>
        <label class="login-field">
          <span>用户名</span>
          <input v-model="username" type="text" placeholder="请输入用户名" autocomplete="username" />
        </label>

        <label class="login-field">
          <span>密码</span>
          <input
            v-model="password"
            type="password"
            placeholder="请输入密码"
            autocomplete="current-password"
          />
        </label>

        <button type="submit" class="login-submit">登录</button>
      </form>

      <p class="login-card__hint">
        当前版本仅用于前端页面搭建，按钮暂不提交，也不会跳转。
      </p>
    </div>
  </section>
</template>
