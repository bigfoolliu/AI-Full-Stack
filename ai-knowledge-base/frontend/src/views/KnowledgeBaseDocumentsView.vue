<script setup lang="ts">
import { onMounted, ref, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { useRoute } from 'vue-router';
import { ElMessage } from 'element-plus';
import { Search } from '@element-plus/icons-vue';
import {
  getKnowledgeBaseDetail,
  getKnowledgeBaseDocuments,
  searchKnowledgeBaseDocuments,
  type KnowledgeBaseDocumentItem,
  type SearchDocumentItem,
} from '../api/knowledge-bases';

const route = useRoute();
const router = useRouter();

const knowledgeBaseId = route.params.id;
const kbName = ref('');
const documents = ref<KnowledgeBaseDocumentItem[]>([]);
const loading = ref(true);
const statusFilter = ref('');

const searchQuery = ref('');
const searchMode = ref(false);
const searchResults = ref<SearchDocumentItem[]>([]);
const searchTotal = ref(0);
const searchPage = ref(1);
const searchPageSize = ref(10);
const searchLoading = ref(false);
let debounceTimer: ReturnType<typeof setTimeout> | null = null;

const goBack = () => {
  router.push('/knowledge-bases');
};

const goToUpload = () => {
  router.push(`/knowledge-bases/${knowledgeBaseId}/upload`);
};

const fetchDocuments = async (status?: string) => {
  loading.value = true;

  try {
    const result = await getKnowledgeBaseDocuments(String(knowledgeBaseId), status || undefined);

    if (result.code !== 0 || !result.data) {
      documents.value = [];
      ElMessage.error(result.message || '获取文档列表失败');
      return;
    }

    documents.value = result.data;
  } catch {
    documents.value = [];
    ElMessage.error('请求文档列表失败，请稍后重试');
  } finally {
    loading.value = false;
  }
};

const executeSearch = async () => {
  searchLoading.value = true;
  try {
    const result = await searchKnowledgeBaseDocuments(String(knowledgeBaseId), {
      q: searchQuery.value.trim(),
      status: statusFilter.value || undefined,
      page: searchPage.value,
      pageSize: searchPageSize.value,
    });

    if (result.code !== 0 || !result.data) {
      searchResults.value = [];
      ElMessage.error(result.message || '搜索失败');
      return;
    }

    searchResults.value = result.data.items;
    searchTotal.value = result.data.total;
    searchPage.value = result.data.page;
    searchPageSize.value = result.data.page_size;
  } catch {
    searchResults.value = [];
    ElMessage.error('搜索请求失败，请稍后重试');
  } finally {
    searchLoading.value = false;
  }
};

const onSearchInput = () => {
  if (debounceTimer) clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => {
    if (searchQuery.value.trim()) {
      searchMode.value = true;
      searchPage.value = 1;
      executeSearch();
    } else {
      searchMode.value = false;
      searchResults.value = [];
      void fetchDocuments(statusFilter.value || undefined);
    }
  }, 300);
};

const onStatusChange = (value: string) => {
  if (searchMode.value) {
    searchPage.value = 1;
    executeSearch();
  } else {
    void fetchDocuments(value || undefined);
  }
};

const onSearchPageChange = (page: number) => {
  searchPage.value = page;
  executeSearch();
};

const statusTagType = (status: string) => {
  if (status === '已完成') return 'success';
  if (status === '解析中') return 'warning';
  return 'info';
};

onMounted(async () => {
  const detail = await getKnowledgeBaseDetail(String(knowledgeBaseId));
  if (detail.code === 0 && detail.data) {
    kbName.value = detail.data.name;
  }
  void fetchDocuments();
});

onUnmounted(() => {
  if (debounceTimer) clearTimeout(debounceTimer);
});
</script>

<template>
  <section class="kb-doc-page">
    <header class="kb-doc-page__header">
      <div>
        <h2>{{ kbName || '文档列表' }}</h2>
        <p>查看当前知识库下的文档处理情况。</p>
      </div>
    </header>

    <div class="kb-doc-context">
      <strong>{{ kbName ? `${kbName} — 文档列表` : '文档列表' }}</strong>
      <el-tag size="small" type="info">ID: {{ route.params.id }}</el-tag>
    </div>

    <div class="kb-doc-actions">
      <el-button @click="goBack">返回知识库列表</el-button>
      <el-input
        v-model="searchQuery"
        class="kb-search"
        placeholder="搜索文档内容..."
        clearable
        :prefix-icon="Search"
        style="width: 240px"
        @input="onSearchInput"
        @clear="onSearchInput"
      />
      <el-select
        v-model="statusFilter"
        placeholder="筛选状态"
        clearable
        style="width: 140px"
        @change="onStatusChange"
      >
        <el-option label="全部" value="" />
        <el-option label="已完成" value="completed" />
        <el-option label="解析中" value="parsing" />
        <el-option label="待处理" value="pending" />
      </el-select>
      <el-button type="primary" @click="goToUpload">去上传文档</el-button>
    </div>

    <template v-if="searchMode">
      <el-table
        v-loading="searchLoading"
        :data="searchResults"
        style="width: 100%"
        empty-text="未搜索到相关文档"
        stripe
      >
        <el-table-column prop="filename" label="文档名称" min-width="160" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="statusTagType(row.status)" size="small">
              {{ row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="内容片段" min-width="300">
          <template #default="{ row }">
            <span class="snippet-text" v-html="row.snippet" />
          </template>
        </el-table-column>
        <el-table-column prop="updated_at" label="更新时间" width="180" />
      </el-table>
      <div v-if="searchTotal > searchPageSize" class="kb-doc-pagination">
        <el-pagination
          v-model:current-page="searchPage"
          :page-size="searchPageSize"
          :total="searchTotal"
          layout="prev, pager, next"
          @current-change="onSearchPageChange"
        />
      </div>
    </template>

    <template v-else>
      <el-table
        v-loading="loading"
        :data="documents"
        style="width: 100%"
        empty-text="当前还没有文档，快去上传一个吧"
        stripe
      >
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
    </template>
  </section>
</template>

<style scoped>
.snippet-text :deep(mark) {
  background-color: #ffd43b;
  color: #1a1a2e;
  padding: 0 2px;
  border-radius: 2px;
}

.kb-doc-pagination {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}

.kb-doc-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}
</style>
