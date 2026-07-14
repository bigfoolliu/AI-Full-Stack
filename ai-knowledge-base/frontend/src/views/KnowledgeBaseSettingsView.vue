<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import {
  getKnowledgeBaseSettings,
  updateKnowledgeBaseSettings,
  getKnowledgeBaseDetail,
} from '../api/knowledge-bases';

const route = useRoute();
const router = useRouter();

const knowledgeBaseId = route.params.id;
const kbName = ref('');
const loading = ref(false);
const saving = ref(false);

const topK = ref(5);
const similarityThreshold = ref(0.0);

const goBack = () => {
  router.push(`/knowledge-bases/${knowledgeBaseId}/documents`);
};

const loadSettings = async () => {
  loading.value = true;
  try {
    const kbRes = await getKnowledgeBaseDetail(String(knowledgeBaseId));
    kbName.value = kbRes.data.name;

    const res = await getKnowledgeBaseSettings(String(knowledgeBaseId));
    topK.value = res.data.top_k;
    similarityThreshold.value = res.data.similarity_threshold;
  } catch {
    ElMessage.error('加载设置失败');
  } finally {
    loading.value = false;
  }
};

const saveSettings = async () => {
  saving.value = true;
  try {
    await updateKnowledgeBaseSettings(String(knowledgeBaseId), {
      top_k: topK.value,
      similarity_threshold: similarityThreshold.value,
    });
    ElMessage.success('设置已保存');
  } catch {
    ElMessage.error('保存设置失败');
  } finally {
    saving.value = false;
  }
};

onMounted(loadSettings);
</script>

<template>
  <section class="kb-settings-page">
    <header class="kb-settings-page__header">
      <el-button text @click="goBack">← 返回文档列表</el-button>
      <h2>检索参数配置</h2>
      <p class="kb-settings-page__subtitle" v-if="kbName">{{ kbName }}</p>
    </header>

    <el-card v-loading="loading" class="kb-settings-card">
      <el-form label-width="160px" label-position="top">
        <el-form-item label="检索数量（Top-k）">
          <div class="kb-settings-page__slider-row">
            <el-slider
              v-model="topK"
              :min="1"
              :max="20"
              :step="1"
              show-stops
              style="width: 300px"
            />
            <span class="kb-settings-page__value">{{ topK }}</span>
          </div>
          <p class="kb-settings-page__hint">
            控制每次检索返回的最大文档片段数。值越大，上下文越丰富，但会增加 Token 消耗。
          </p>
        </el-form-item>

        <el-form-item label="相似度阈值">
          <div class="kb-settings-page__slider-row">
            <el-slider
              v-model="similarityThreshold"
              :min="0"
              :max="1"
              :step="0.05"
              show-stops
              style="width: 300px"
            />
            <span class="kb-settings-page__value">{{ similarityThreshold.toFixed(2) }}</span>
          </div>
          <p class="kb-settings-page__hint">
            仅返回相似度得分达到该阈值的文档片段。设为 0 表示不进行过滤。
          </p>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" :loading="saving" @click="saveSettings">
            {{ saving ? '保存中...' : '保存设置' }}
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </section>
</template>

<style scoped>
.kb-settings-page {
  max-width: 720px;
  margin: 0 auto;
  padding: 24px;
}

.kb-settings-page__header {
  margin-bottom: 24px;
}

.kb-settings-page__header h2 {
  margin: 8px 0 0;
}

.kb-settings-page__subtitle {
  color: #909399;
  font-size: 14px;
  margin: 4px 0 0;
}

.kb-settings-card {
  padding: 8px;
}

.kb-settings-page__slider-row {
  display: flex;
  align-items: center;
  gap: 16px;
}

.kb-settings-page__value {
  font-size: 18px;
  font-weight: 600;
  color: #409eff;
  min-width: 36px;
}

.kb-settings-page__hint {
  color: #909399;
  font-size: 12px;
  margin: 4px 0 0;
  line-height: 1.5;
}
</style>
