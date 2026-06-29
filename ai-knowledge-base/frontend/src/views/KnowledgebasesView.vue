<script setup lang="ts">
import { onMounted, ref } from "vue";
import {
  getKnowledgeBases,
  type KnowledgeBaseItem,
} from "../api/knowledge-bases";

const knowledgeBases = ref<KnowledgeBaseItem[]>([]);
const loading = ref(true);
const error = ref("");

const fetchKnowledgeBases = async () => {
  loading.value = true;
  error.value = "";

  try {
    const result = await getKnowledgeBases();

    if (result.code !== 0 || !result.data) {
      knowledgeBases.value = [];
      error.value = result.message || "获取知识库列表失败";
      return;
    }

    knowledgeBases.value = result.data;
  } catch {
    knowledgeBases.value = [];
    error.value = "请求知识库列表失败，请稍后重试";
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  void fetchKnowledgeBases();
});
</script>

<template>
  <section class="kb-page">
    <header class="kb-page__header">
      <div>
        <h2>知识库列表</h2>
        <p>集中管理你的文档知识库，后续这里会接入真实搜索、上传和状态流转能力。</p>
      </div>
    </header>

    <div class="kb-toolbar">
      <input class="kb-search" type="text" placeholder="搜索知识库名称" />
      <button type="button" class="kb-create-button">新建知识库</button>
    </div>

    <div v-if="loading" class="kb-state-card">
      <p>知识库列表加载中...</p>
    </div>

    <div v-else-if="error" class="kb-state-card kb-state-card--error">
      <p>{{ error }}</p>
    </div>

    <div v-else-if="knowledgeBases.length === 0" class="kb-state-card">
      <strong>还没有知识库</strong>
      <p>先创建第一个知识库，后续这里会显示真实列表数据。</p>
    </div>

    <div v-else class="kb-table-card">
      <table class="kb-table">
        <thead>
          <tr>
            <th>名称</th>
            <th>描述</th>
            <th>文档数量</th>
            <th>创建时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in knowledgeBases" :key="item.id">
            <td>
              <div class="kb-name-cell">
                <strong>{{ item.name }}</strong>
                <span>知识库 ID：{{ item.id }}</span>
              </div>
            </td>
            <td>{{ item.description }}</td>
            <td>{{ item.document_count }}</td>
            <td>{{ item.created_at }}</td>
            <td>
              <div class="kb-actions">
                <button type="button">查看</button>
                <button type="button">编辑</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <p class="kb-page__hint">
      当前列表已经由后端接口驱动，后续可继续扩展搜索、分页和新建知识库流程。
    </p>
  </section>
</template>
