<script setup lang="ts">
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import MarkdownIt from 'markdown-it';
import { http } from '../api/http';

const md = new MarkdownIt({ html: false, breaks: true });
const route = useRoute();
const router = useRouter();
const kbId = route.params.id as string;

const query = ref('');
const loadingA = ref(false);
const loadingB = ref(false);
const resultA = ref<any>(null);
const resultB = ref<any>(null);

const configA = ref({
  top_k: 5,
  similarity_threshold: 0.0,
  hybrid_search: false,
  hybrid_alpha: 0.3,
  rerank_enabled: false,
  rerank_top_k: 5,
  temperature: 0.7,
});

const configB = ref({
  top_k: 10,
  similarity_threshold: 0.3,
  hybrid_search: true,
  hybrid_alpha: 0.3,
  rerank_enabled: true,
  rerank_top_k: 5,
  temperature: 0.7,
});

const runCompare = async () => {
  if (!query.value.trim()) return;
  loadingA.value = true;
  loadingB.value = true;
  resultA.value = null;
  resultB.value = null;

  try {
    const id = Number(kbId);
    const resA = await http.post(`/api/knowledge-bases/${id}/chat`, {
      query: query.value,
      top_k: configA.value.top_k,
      filter: { status: 'completed' },
    });
    resultA.value = resA.data.data;

    const resB = await http.post(`/api/knowledge-bases/${id}/chat`, {
      query: query.value,
      top_k: configB.value.top_k,
      filter: { status: 'completed' },
    });
    resultB.value = resB.data.data;
  } catch (err: any) {
    ElMessage.error(err?.response?.data?.detail || '请求失败');
  } finally {
    loadingA.value = false;
    loadingB.value = false;
  }
};

const goBack = () => router.push(`/knowledge-bases/${kbId}/chat`);

const formatScore = (s: number) => (s * 100).toFixed(1) + '%';

const labelA = '配置 A（当前）';
const labelB = '配置 B（对比）';
</script>

<template>
  <section class="compare-page">
    <header class="compare-header">
      <el-button text @click="goBack">← 返回聊天</el-button>
      <h2>效果对比</h2>
      <p>使用不同参数配置对同一问题提问，对比回答效果。</p>
    </header>

    <el-card class="compare-input-card">
      <el-input v-model="query" type="textarea" :rows="3" placeholder="输入问题..." />
      <el-button
        type="primary"
        :loading="loadingA || loadingB"
        :disabled="!query.trim()"
        @click="runCompare"
        style="margin-top: 12px"
      >
        {{ loadingA || loadingB ? '请求中...' : '对比回答' }}
      </el-button>
    </el-card>

    <div v-if="resultA || resultB" class="compare-results">
      <div class="compare-col">
        <h3 class="compare-col__title">{{ labelA }}</h3>
        <el-card v-if="resultA" class="compare-col__card">
          <div class="compare-metrics">
            <el-tag size="small" v-if="resultA.metrics">
              命中 {{ resultA.metrics.used_chunks }} 条 | 最高分 {{ resultA.metrics.score_max }} |
              耗时 {{ resultA.metrics.time_ms }}ms
            </el-tag>
          </div>
          <div class="compare-answer" v-html="md.render(resultA.answer || '')" />
          <div v-if="resultA.sources?.length" class="compare-sources">
            <div class="compare-sources__title">来源 ({{ resultA.sources.length }})</div>
            <div v-for="(s, i) in resultA.sources" :key="i" class="compare-source-item">
              <span class="compare-source-item__file">{{ s.filename }}</span>
              <span class="compare-source-item__score">{{ formatScore(s.score) }}</span>
            </div>
          </div>
        </el-card>
        <div v-else-if="loadingA" class="compare-col__loading">请求中...</div>
      </div>

      <div class="compare-col">
        <h3 class="compare-col__title">{{ labelB }}</h3>
        <el-card v-if="resultB" class="compare-col__card">
          <div class="compare-metrics">
            <el-tag size="small" v-if="resultB.metrics">
              命中 {{ resultB.metrics.used_chunks }} 条 | 最高分 {{ resultB.metrics.score_max }} |
              耗时 {{ resultB.metrics.time_ms }}ms
            </el-tag>
          </div>
          <div class="compare-answer" v-html="md.render(resultB.answer || '')" />
          <div v-if="resultB.sources?.length" class="compare-sources">
            <div class="compare-sources__title">来源 ({{ resultB.sources.length }})</div>
            <div v-for="(s, i) in resultB.sources" :key="i" class="compare-source-item">
              <span class="compare-source-item__file">{{ s.filename }}</span>
              <span class="compare-source-item__score">{{ formatScore(s.score) }}</span>
            </div>
          </div>
        </el-card>
        <div v-else-if="loadingB" class="compare-col__loading">请求中...</div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.compare-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
}

.compare-header {
  margin-bottom: 20px;
}

.compare-header h2 {
  margin: 8px 0 0;
}

.compare-input-card {
  margin-bottom: 24px;
}

.compare-results {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.compare-col__title {
  margin: 0 0 8px;
  font-size: 15px;
}

.compare-col__card {
  padding: 8px;
}

.compare-col__loading {
  color: #909399;
  padding: 24px;
  text-align: center;
}

.compare-metrics {
  margin-bottom: 12px;
}

.compare-answer {
  line-height: 1.7;
  font-size: 14px;
  word-break: break-word;
}

.compare-answer :deep(p) {
  margin: 0 0 8px;
}

.compare-sources {
  margin-top: 16px;
  padding-top: 12px;
  border-top: 1px solid #e2e8f0;
}

.compare-sources__title {
  font-size: 12px;
  color: #94a3b8;
  font-weight: 600;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.compare-source-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 8px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  margin-bottom: 4px;
  font-size: 13px;
}

.compare-source-item__file {
  color: #0f172a;
  font-weight: 500;
}

.compare-source-item__score {
  color: #2563eb;
}
</style>
