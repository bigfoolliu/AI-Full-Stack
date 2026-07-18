<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { getKnowledgeBases, type KnowledgeBaseItem } from '../api/knowledge-bases';
import { toastError } from '../utils/toast';

const loading = ref(true);
const kbCount = ref(0);
const docCount = ref(0);
const recentKBs = ref<KnowledgeBaseItem[]>([]);

onMounted(async () => {
  try {
    const result = await getKnowledgeBases(1, 100);
    if (result.code === 0 && result.data) {
      recentKBs.value = result.data.items.slice(0, 3);
      kbCount.value = result.data.total;
      docCount.value = result.data.items.reduce((sum, kb) => sum + (kb.document_count || 0), 0);
    }
  } catch {
    toastError('加载数据失败');
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <section class="dashboard-page">
    <header class="dashboard-hero">
      <div>
        <p class="dashboard-hero__eyebrow">Workspace Overview</p>
        <h2>欢迎回来，今天继续把 AI 知识库项目往前推进。</h2>
        <p class="dashboard-hero__description">查看知识库概览和待处理任务。</p>
      </div>
    </header>

    <div class="dashboard-summary">
      <el-card v-loading="loading" shadow="hover">
        <el-statistic :value="kbCount" title="知识库总数" />
      </el-card>
      <el-card v-loading="loading" shadow="hover">
        <el-statistic :value="docCount" title="文档总数" />
      </el-card>
      <el-card v-loading="loading" shadow="hover">
        <el-statistic :value="recentKBs.length" title="最近活跃" />
      </el-card>
    </div>

    <div class="dashboard-panels">
      <el-card shadow="never">
        <template #header>
          <span>最近更新的知识库</span>
        </template>
        <div v-if="loading">
          <div v-for="i in 3" :key="i" class="dashboard-skeleton" />
        </div>
        <div v-else-if="recentKBs.length === 0">
          <p style="color: #94a3b8; font-size: 14px; text-align: center; padding: 24px 0">
            暂无知识库
          </p>
        </div>
        <div v-for="item in recentKBs" :key="item.id" class="dashboard-list-item">
          <div>
            <strong>{{ item.name }}</strong>
            <p>{{ item.created_at || '' }}</p>
          </div>
          <el-tag size="small" :type="item.document_count ? 'success' : 'info'">
            {{ item.document_count || 0 }} 文档
          </el-tag>
        </div>
      </el-card>

      <el-card shadow="never">
        <template #header>
          <span>快速开始</span>
        </template>
        <div class="dashboard-quick-actions">
          <el-button type="primary" @click="$router.push('/knowledge-bases/create')">
            新建知识库
          </el-button>
          <el-button @click="$router.push('/knowledge-bases')"> 浏览知识库 </el-button>
        </div>
        <el-divider />
        <p style="color: #94a3b8; font-size: 13px; line-height: 1.6">
          上传文档到知识库后，即可通过问答页面进行智能检索和 AI 问答。
        </p>
      </el-card>
    </div>
  </section>
</template>

<style scoped>
.dashboard-skeleton {
  height: 40px;
  margin: 10px 0;
  border-radius: 8px;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

.dashboard-quick-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}
</style>
