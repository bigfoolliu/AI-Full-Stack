<script setup lang="ts">
import { ref, onErrorCaptured } from 'vue';

const hasError = ref(false);
const errorMessage = ref('');

onErrorCaptured((err) => {
  hasError.value = true;
  errorMessage.value = err.message || '发生未知错误';
  return false;
});

const reset = () => {
  hasError.value = false;
  errorMessage.value = '';
};
</script>

<template>
  <div v-if="hasError" class="error-boundary">
    <div class="error-boundary__card">
      <div class="error-boundary__icon">!</div>
      <h2 class="error-boundary__title">页面渲染出错</h2>
      <p class="error-boundary__message">{{ errorMessage }}</p>
      <p class="error-boundary__hint">请尝试刷新页面，或返回其他页面</p>
      <div class="error-boundary__actions">
        <button class="error-boundary__btn error-boundary__btn--primary" @click="reset">
          重试
        </button>
        <button class="error-boundary__btn" @click="$router.back()">返回上一页</button>
      </div>
    </div>
  </div>
  <slot v-else />
</template>

<style scoped>
.error-boundary {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  padding: 40px;
}

.error-boundary__card {
  background: #ffffff;
  border: 1px solid #fecaca;
  border-radius: 16px;
  padding: 40px;
  max-width: 480px;
  width: 100%;
  text-align: center;
  box-shadow: 0 8px 24px rgba(239, 68, 68, 0.08);
}

.error-boundary__icon {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: #fef2f2;
  color: #ef4444;
  font-size: 28px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
}

.error-boundary__title {
  font-size: 20px;
  margin-bottom: 8px;
}

.error-boundary__message {
  color: #64748b;
  font-size: 14px;
  margin-bottom: 4px;
}

.error-boundary__hint {
  color: #94a3b8;
  font-size: 13px;
  margin-bottom: 24px;
}

.error-boundary__actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.error-boundary__btn {
  padding: 8px 20px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  background: #ffffff;
  color: #374151;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.15s;
}

.error-boundary__btn:hover {
  background: #f9fafb;
}

.error-boundary__btn--primary {
  background: #2563eb;
  color: #ffffff;
  border-color: #2563eb;
}

.error-boundary__btn--primary:hover {
  background: #1d4ed8;
}
</style>
