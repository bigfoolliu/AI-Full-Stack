<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { useRoute } from "vue-router";
import { ElMessage } from "element-plus";
import {
  getKnowledgeBaseDocuments,
  type KnowledgeBaseDocumentItem,
} from "../api/knowledge-bases";

const route = useRoute();
const router = useRouter();

const knowledgeBaseId = route.params.id;
const documents = ref<KnowledgeBaseDocumentItem[]>([]);
const loading = ref(true);

const goBack = () => {
  router.push("/knowledge-bases");
};

const goToUpload = () => {
  router.push(`/knowledge-bases/${knowledgeBaseId}/upload`);
};

const fetchDocuments = async () => {
  loading.value = true;

  try {
    const result = await getKnowledgeBaseDocuments(String(knowledgeBaseId));

    if (result.code !== 0 || !result.data) {
      documents.value = [];
      ElMessage.error(result.message || "获取文档列表失败");
      return;
    }

    documents.value = result.data;
  } catch {
    documents.value = [];
    ElMessage.error("请求文档列表失败，请稍后重试");
  } finally {
    loading.value = false;
  }
};

const statusTagType = (status: string) => {
  if (status === "已完成") return "success";
  if (status === "解析中") return "warning";
  return "info";
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
        <p>查看当前知识库下的文档处理情况。</p>
      </div>
    </header>

    <div class="kb-doc-context">
      <strong>当前知识库 ID：{{ route.params.id }}</strong>
    </div>

    <div class="kb-doc-actions">
      <el-button @click="goBack">返回知识库列表</el-button>
      <el-button type="primary" @click="goToUpload">去上传文档</el-button>
    </div>

    <el-table v-loading="loading" :data="documents" style="width: 100%" empty-text="当前还没有文档，快去上传一个吧" stripe>
      <el-table-column prop="name" label="文档名称" min-width="200" />
      <el-table-column label="状态" width="120">
        <template #default="{ row }">
          <el-tag :type="statusTagType(row.status)" size="small">
            {{ row.status }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="updated_at" label="更新时间" width="180" />
      <el-table-column label="操作" width="150">
        <template #default>
          <el-button size="small">查看</el-button>
          <el-button size="small">重试</el-button>
        </template>
      </el-table-column>
    </el-table>
  </section>
</template>
