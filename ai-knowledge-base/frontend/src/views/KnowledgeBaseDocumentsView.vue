<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { useRoute } from "vue-router";
import {
  getKnowledgeBaseDocuments,
  type KnowledgeBaseDocumentItem,
} from "../api/knowledge-bases";

const route = useRoute();
const router = useRouter();

const knowledgeBaseId = route.params.id;
const documents = ref<KnowledgeBaseDocumentItem[]>([]);
const loading = ref(true);
const errorMessage = ref("");

const goBack = () => {
  router.push("/knowledge-bases");
};

const goToUpload = () => {
  router.push(`/knowledge-bases/${knowledgeBaseId}/upload`);
};

const fetchDocuments = async () => {
  loading.value = true;
  errorMessage.value = "";

  try {
    const result = await getKnowledgeBaseDocuments(String(knowledgeBaseId));

    if (result.code !== 0 || !result.data) {
      documents.value = [];
      errorMessage.value = result.message || "获取文档列表失败";
      return;
    }

    documents.value = result.data;
  } catch {
    documents.value = [];
    errorMessage.value = "请求文档列表失败，请稍后重试";
  } finally {
    loading.value = false;
  }
};

const getStatusClass = (status: string) => {
  if (status === "已完成") return "kb-doc-status--success";
  if (status === "解析中") return "kb-doc-status--processing";
  return "kb-doc-status--pending";
};

onMounted(() => {
  void fetchDocuments();
});
</script>

<template>
  <section class="kb-doc-page">
    <header class="kb-doc-page__header">
      <div>
        <h2>文档列表 / 状态页</h2>
        <p>查看当前知识库下的文档处理情况，并继续推进上传与解析流程。</p>
      </div>
    </header>

    <div class="kb-doc-context">
      <strong>当前知识库 ID：{{ route.params.id }}</strong>
      <p>这里后续会继续补充当前知识库名称、说明和统计信息。</p>
    </div>

    <div class="kb-doc-actions">
      <button type="button" class="kb-secondary-button" @click="goBack">
        返回知识库列表
      </button>
      <button type="button" class="kb-primary-button" @click="goToUpload">
        去上传文档
      </button>
    </div>

    <div v-if="loading" class="kb-state-card">
      <p>文档列表加载中...</p>
    </div>

    <div v-else-if="errorMessage" class="kb-state-card kb-state-card--error">
      <p>{{ errorMessage }}</p>
    </div>

    <div v-else-if="documents.length === 0" class="kb-state-card">
      <strong>当前还没有文档</strong>
      <p>先上传一个文档，后续这里会展示真实处理状态。</p>
    </div>

    <div v-else class="kb-doc-table-card">
      <table class="kb-doc-table">
        <thead>
          <tr>
            <th>文档名称</th>
            <th>状态</th>
            <th>更新时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in documents" :key="item.id">
            <td>{{ item.name }}</td>
            <td>
              <span class="kb-doc-status" :class="getStatusClass(item.status)">
                {{ item.status }}
              </span>
            </td>
            <td>{{ item.updated_at }}</td>
            <td>
              <div class="kb-actions">
                <button type="button">查看</button>
                <button type="button">重试</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>
