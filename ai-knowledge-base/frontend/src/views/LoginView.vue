<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { useUserStore } from '../stores/user'

const router = useRouter()
const userStore = useUserStore()

const formRef = ref<FormInstance>()

const form = reactive({
  username: '',
  password: '',
})

const rules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 2, max: 50, message: '用户名长度为 2-50 个字符', trigger: 'blur' },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 4, max: 50, message: '密码长度为 4-50 个字符', trigger: 'blur' },
  ],
}

const handleLogin = async () => {
  if (!formRef.value) return

  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  userStore.clearError()

  const success = await userStore.login(form.username.trim(), form.password.trim())

  if (success) {
    ElMessage.success('登录成功')
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
          输入账号密码登录知识库系统。
        </p>
      </div>

      <el-form ref="formRef" :model="form" :rules="rules" label-position="top" @submit.prevent="handleLogin">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名" autocomplete="username" />
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" autocomplete="current-password" show-password />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" native-type="submit" :loading="userStore.loginLoading" style="width: 100%">
            {{ userStore.loginLoading ? '登录中...' : '登录' }}
          </el-button>
        </el-form-item>
      </el-form>

      <el-alert v-if="userStore.loginError" :title="userStore.loginError" type="error" show-icon :closable="false" />

      <p class="login-card__hint">
        Demo 账号：`admin`，密码：`123456`
      </p>
    </div>
  </section>
</template>
