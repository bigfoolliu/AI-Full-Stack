<script setup lang="ts">
defineProps<{
  icon?: string;
  title?: string;
  description?: string;
}>();
</script>

<template>
  <div class="empty-state">
    <div class="empty-state__icon">{{ icon || '📭' }}</div>
    <h3 class="empty-state__title">{{ title || '暂无数据' }}</h3>
    <p v-if="description" class="empty-state__description">{{ description }}</p>
    <div v-if="$slots.action" class="empty-state__action">
      <slot name="action" />
    </div>
  </div>
</template>

<style scoped>
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 24px;
  text-align: center;
}

.empty-state__icon {
  font-size: 48px;
  margin-bottom: 16px;
  line-height: 1;
}

.empty-state__title {
  font-size: 18px;
  color: #1e293b;
  margin-bottom: 8px;
}

.empty-state__description {
  font-size: 14px;
  color: #94a3b8;
  max-width: 360px;
  line-height: 1.6;
}

.empty-state__action {
  margin-top: 20px;
}
</style>
