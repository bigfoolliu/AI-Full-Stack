<script setup lang="ts">
import { useRoute } from "vue-router";

const route = useRoute();
</script>

<template>
  <section class="kb-placeholder-page">
    <h2>文档列表 / 状态页</h2>
    <p>当前知识库 ID：{{ route.params.id }}</p>
    <p>这里将用于展示当前知识库下的文档列表、状态和后续处理入口。</p>
  </section>
</template>
