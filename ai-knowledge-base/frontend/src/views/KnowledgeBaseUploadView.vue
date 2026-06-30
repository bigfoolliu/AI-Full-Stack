<script setup lang="ts">
import { useRoute } from "vue-router";

const route = useRoute();
</script>

<template>
  <section class="kb-placeholder-page">
    <h2>文档上传页</h2>
    <p>当前知识库 ID：{{ route.params.id }}</p>
    <p>这里将用于上传文档并接入后续解析流程。Day 1 先把路径和页面占位搭好。</p>
  </section>
</template>
