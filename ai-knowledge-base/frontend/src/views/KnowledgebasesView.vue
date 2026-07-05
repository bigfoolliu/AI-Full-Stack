<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import {
  getKnowledgeBases,
  type KnowledgeBaseItem,
} from "../api/knowledge-bases";

const router = useRouter();
const knowledgeBases = ref<KnowledgeBaseItem[]>([]);
const loading = ref(true);
const currentPage = ref(1);
const pageSize = ref(10);
const total = ref(0);

const fetchKnowledgeBases = async () => {
  loading.value = true;

  try {
    const result = await getKnowledgeBases(currentPage.value, pageSize.value);

    if (result.code !== 0 || !result.data) {
      ElMessage.error(result.message || "获取知识库列表失败");
      knowledgeBases.value = [];
      return;
    }

    knowledgeBases.value = result.data.items;
    total.value = result.data.total;
  } catch {
    ElMessage.error("请求知识库列表失败，请稍后重试");
    knowledgeBases.value = [];
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  void fetchKnowledgeBases();
});

const goToCreate = () => {
  router.push("/knowledge-bases/create");
};

const goToDocuments = (id: number) => {
  router.push(`/knowledge-bases/${id}/documents`);
};

const goToUpload = (id: number) => {
  router.push(`/knowledge-bases/${id}/upload`);
};

const onPageChange = (page: number) => {
  currentPage.value = page;
  void fetchKnowledgeBases();
};
</script>

<template>
  <section class="kb-page">
    <header class="kb-page__header">
      <div>
        <h2>知识库列表</h2>
        <p>集中管理你的文档知识库。</p>
      </div>
    </header>

    <div class="kb-toolbar">
      <el-input
        class="kb-search"
        placeholder="搜索知识库名称"
        clearable
      />
      <el-button type="primary" @click="goToCreate">
        新建知识库
      </el-button>
    </div>

    <el-table
      v-loading="loading"
      :data="knowledgeBases"
      style="width: 100%"
      empty-text="还没有知识库，先创建一个吧"
      stripe
    >
      <el-table-column label="名称" min-width="180">
        <template #default="{ row }">
          <div class="kb-name-cell">
            <strong>{{ row.name }}</strong>
            <span>知识库 ID：{{ row.id }}</span>
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="description" label="描述" min-width="200" />
      <el-table-column prop="document_count" label="文档数量" width="100" />
      <el-table-column prop="created_at" label="创建时间" width="180" />
      <el-table-column label="操作" width="150">
        <template #default="{ row }">
          <el-button size="small" @click="goToDocuments(row.id)">查看</el-button>
          <el-button size="small" @click="goToUpload(row.id)">上传</el-button>
        </template>
      </el-table-column>
    </el-table>

    <div style="display: flex; justify-content: center; margin-top: 16px;">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[5, 10, 20]"
        layout="total, sizes, prev, pager, next"
        @current-change="onPageChange"
        @size-change="onPageChange"
      />
    </div>
  </section>
</template>
