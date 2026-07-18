<script setup lang="ts">
import { onMounted, ref, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { useRoute } from 'vue-router';
import { ElMessage } from 'element-plus';
import { Search } from '@element-plus/icons-vue';
import EmptyState from '../components/EmptyState.vue';
import {
  getKnowledgeBaseDetail,
  getKnowledgeBaseDocuments,
  searchKnowledgeBaseDocuments,
  processDocument,
  getDocumentContent,
  type KnowledgeBaseDocumentItem,
  type SearchDocumentItem,
  type DocumentContentItem,
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

const processLoadingId = ref<number | null>(null);
let processPollTimer: ReturnType<typeof setInterval> | null = null;

const contentDialogVisible = ref(false);
const contentDialogLoading = ref(false);
const contentItem = ref<DocumentContentItem | null>(null);

const goBack = () => {
  router.push('/knowledge-bases');
};

const goToUpload = () => {
  router.push(`/knowledge-bases/${knowledgeBaseId}/upload`);
};

const goToChat = () => {
  router.push(`/knowledge-bases/${knowledgeBaseId}/chat`);
};

const goToSettings = () => {
  router.push(`/knowledge-bases/${knowledgeBaseId}/settings`);
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

    documents.value = result.data?.items || [];
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
  if (status === '处理中') return 'warning';
  if (status === '处理失败') return 'danger';
  return 'info';
};

const startProcessPoll = () => {
  if (processPollTimer) clearInterval(processPollTimer);
  processPollTimer = setInterval(async () => {
    await fetchDocuments(statusFilter.value || undefined);
    const hasProcessing = documents.value.some((d) => d.status === '处理中');
    if (!hasProcessing) {
      if (processPollTimer) {
        clearInterval(processPollTimer);
        processPollTimer = null;
      }
      processLoadingId.value = null;
    }
  }, 2000);
};

const handleProcess = async (docId: number) => {
  processLoadingId.value = docId;
  try {
    const result = await processDocument(docId);
    if (result.code !== 0) {
      ElMessage.error(result.message || '处理失败');
      processLoadingId.value = null;
      return;
    }
    ElMessage.success('处理完成');
    await fetchDocuments(statusFilter.value || undefined);
    if (documents.value.some((d) => d.status === '处理中')) {
      startProcessPoll();
    } else {
      processLoadingId.value = null;
    }
  } catch {
    ElMessage.error('处理请求失败');
    processLoadingId.value = null;
  }
};

const handleViewContent = async (docId: number) => {
  contentDialogLoading.value = true;
  contentDialogVisible.value = true;
  try {
    const result = await getDocumentContent(String(knowledgeBaseId), docId);
    if (result.code === 0 && result.data) {
      contentItem.value = result.data;
    } else {
      contentItem.value = null;
      ElMessage.error(result.message || '获取内容失败');
    }
  } catch {
    contentItem.value = null;
    ElMessage.error('获取内容失败');
  } finally {
    contentDialogLoading.value = false;
  }
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
  if (processPollTimer) clearInterval(processPollTimer);
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
        <el-option label="处理中" value="processing" />
        <el-option label="待处理" value="pending" />
        <el-option label="处理失败" value="failed" />
      </el-select>
      <el-button type="success" @click="goToChat">去问答</el-button>
      <el-button type="primary" @click="goToUpload">去上传文档</el-button>
      <el-button @click="goToSettings">检索设置</el-button>
    </div>

    <template v-if="searchMode">
      <el-table v-loading="searchLoading" :data="searchResults" style="width: 100%" stripe>
        <template #empty>
          <EmptyState title="未搜索到相关文档" description="尝试其他关键词" />
        </template>
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
      <el-table v-loading="loading" :data="documents" style="width: 100%" stripe>
        <template #empty>
          <EmptyState title="当前还没有文档" description="上传一个文档开始吧">
            <template #action>
              <el-button
                type="primary"
                @click="$router.push(`/knowledge-bases/${route.params.id}/upload`)"
                >上传文档</el-button
              >
            </template>
          </EmptyState>
        </template>
        <el-table-column prop="name" label="文档名称" min-width="200" />
        <el-table-column label="状态" width="120">
          <template #default="{ row }">
            <el-tag :type="statusTagType(row.status)" size="small">
              {{ row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="updated_at" label="更新时间" width="180" />
        <el-table-column label="操作" width="180">
          <template #default="{ row }">
            <el-button size="small" @click="handleViewContent(row.id)">查看</el-button>
            <el-button
              size="small"
              type="primary"
              :loading="processLoadingId === row.id"
              :disabled="processLoadingId === row.id"
              @click="handleProcess(row.id)"
            >
              {{ processLoadingId === row.id ? '处理中' : '处理' }}
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </template>
    <el-dialog
      v-model="contentDialogVisible"
      :title="contentItem?.name || '文档内容'"
      width="700px"
      top="5vh"
    >
      <div v-loading="contentDialogLoading" class="content-preview">
        <pre v-if="contentItem?.content" class="content-text">{{ contentItem.content }}</pre>
        <el-empty v-else description="暂无内容" />
      </div>
    </el-dialog>
  </section>
</template>

<style scoped>
.content-preview {
  min-height: 200px;
}

.content-text {
  white-space: pre-wrap;
  word-break: break-word;
  font-size: 14px;
  line-height: 1.7;
  margin: 0;
  max-height: 60vh;
  overflow-y: auto;
}

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
