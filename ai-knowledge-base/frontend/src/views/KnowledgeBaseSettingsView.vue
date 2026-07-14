<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import {
  getKnowledgeBaseSettings,
  updateKnowledgeBaseSettings,
  getKnowledgeBaseDetail,
  listModels,
  type ModelOption,
} from '../api/knowledge-bases';

const route = useRoute();
const router = useRouter();

const knowledgeBaseId = route.params.id;
const kbName = ref('');
const loading = ref(false);
const saving = ref(false);

const topK = ref(5);
const similarityThreshold = ref(0.0);
const systemPrompt = ref('');
const temperature = ref(0.7);
const maxTokens = ref(2048);
const modelName = ref('');
const models = ref<ModelOption[]>([]);

const DEFAULT_SYSTEM_PROMPT = `你是一个知识库问答助手。
请基于以下检索到的文档内容回答用户的问题。
如果文档内容不足以回答，请如实告知，不要编造。`;

const goBack = () => {
  router.push(`/knowledge-bases/${knowledgeBaseId}/documents`);
};

const loadSettings = async () => {
  loading.value = true;
  try {
    const kbRes = await getKnowledgeBaseDetail(String(knowledgeBaseId));
    kbName.value = kbRes.data.name;

    const [res, modelsRes] = await Promise.all([
      getKnowledgeBaseSettings(String(knowledgeBaseId)),
      listModels(),
    ]);
    topK.value = res.data.top_k;
    similarityThreshold.value = res.data.similarity_threshold;
    systemPrompt.value = res.data.system_prompt || '';
    temperature.value = res.data.temperature;
    maxTokens.value = res.data.max_tokens;
    modelName.value = res.data.model_name || '';
    models.value = modelsRes.data;
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
      system_prompt: systemPrompt.value || null,
      temperature: temperature.value,
      max_tokens: maxTokens.value,
      model_name: modelName.value || null,
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

        <el-form-item label="系统指令（System Prompt）">
          <el-input
            v-model="systemPrompt"
            type="textarea"
            :rows="8"
            placeholder="自定义系统指令，留空将使用默认 Prompt"
          />
          <div class="kb-settings-page__prompt-footer">
            <p class="kb-settings-page__hint">
              设置 AI 助手的角色和行为。当产生上下文时，检索到的内容会自动追加到指令末尾。
            </p>
            <el-button text size="small" @click="systemPrompt = DEFAULT_SYSTEM_PROMPT">
              恢复默认
            </el-button>
          </div>
        </el-form-item>

        <el-divider />

        <h3 class="kb-settings-page__section-title">模型参数</h3>

        <el-form-item label="模型选择">
          <el-select v-model="modelName" placeholder="使用默认模型" clearable style="width: 300px">
            <el-option v-for="m in models" :key="m.id" :label="m.name" :value="m.id" />
          </el-select>
          <p class="kb-settings-page__hint">选择 LLM 模型。留空则使用服务端默认模型。</p>
        </el-form-item>

        <el-form-item label="Temperature（温度）">
          <div class="kb-settings-page__slider-row">
            <el-slider
              v-model="temperature"
              :min="0"
              :max="2"
              :step="0.1"
              show-stops
              style="width: 300px"
            />
            <span class="kb-settings-page__value">{{ temperature.toFixed(1) }}</span>
          </div>
          <p class="kb-settings-page__hint">控制输出的随机性。值越低越确定，值越高越有创造性。</p>
        </el-form-item>

        <el-form-item label="Max Tokens">
          <div class="kb-settings-page__slider-row">
            <el-input-number v-model="maxTokens" :min="256" :max="8192" :step="256" />
          </div>
          <p class="kb-settings-page__hint">单次回答的最大 Token 数。范围 256-8192。</p>
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

.kb-settings-page__section-title {
  margin: 0 0 16px;
  font-size: 16px;
}

.kb-settings-page__prompt-footer {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}
</style>
