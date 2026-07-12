<script setup lang="ts">
import { computed, nextTick, onMounted, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import MarkdownIt from 'markdown-it';
import { chatStream, getKnowledgeBaseDetail } from '../api/knowledge-bases';

const md = new MarkdownIt({ html: false, breaks: true });

const mdRenderer = (text: string) => md.render(text);

interface SourceItem {
  filename: string;
  content: string;
  score: number;
  page_number?: number;
}

interface Message {
  role: 'user' | 'assistant';
  content: string;
  sources?: SourceItem[];
  timestamp: number;
}

const route = useRoute();
const router = useRouter();
const knowledgeBaseId = route.params.id as string;
const kbName = ref('');

const messages = ref<Message[]>([]);
const inputText = ref('');
const loading = ref(false);
const currentAnswer = ref('');
const currentSources = ref<SourceItem[]>([]);
const error = ref('');
const abortController = ref<AbortController | null>(null);

const messageListRef = ref<HTMLElement | null>(null);

const history = computed(() => messages.value.map((m) => ({ role: m.role, content: m.content })));

const scrollToBottom = async () => {
  await nextTick();
  if (messageListRef.value) {
    messageListRef.value.scrollTop = messageListRef.value.scrollHeight;
  }
};

watch([messages, currentAnswer], scrollToBottom, { deep: true });

const sendMessage = async () => {
  const text = inputText.value.trim();
  if (!text || loading.value) return;

  inputText.value = '';
  error.value = '';

  messages.value.push({
    role: 'user',
    content: text,
    timestamp: Date.now(),
  });

  loading.value = true;
  currentAnswer.value = '';
  currentSources.value = [];

  abortController.value = chatStream(
    Number(knowledgeBaseId),
    { query: text, history: history.value, top_k: 5 },
    {
      onToken: (token: string) => {
        currentAnswer.value += token;
      },
      onSources: (sources: SourceItem[]) => {
        currentSources.value = sources;
      },
      onDone: () => {
        messages.value.push({
          role: 'assistant',
          content: currentAnswer.value,
          sources: currentSources.value,
          timestamp: Date.now(),
        });
        currentAnswer.value = '';
        currentSources.value = [];
        loading.value = false;
        abortController.value = null;
      },
      onError: (err: Error) => {
        error.value = err.message || '请求失败，请重试';
        loading.value = false;
        abortController.value = null;
      },
    },
  );
};

const retry = () => {
  const lastUserMsg = [...messages.value].reverse().find((m) => m.role === 'user');
  if (lastUserMsg) {
    inputText.value = lastUserMsg.content;
    messages.value = messages.value.filter((m) => m !== lastUserMsg);
    const lastAssistantIdx = messages.value.length - 1;
    if (lastAssistantIdx >= 0 && messages.value[lastAssistantIdx].role === 'assistant') {
      messages.value.pop();
    }
  }
  error.value = '';
};

const newChat = () => {
  messages.value = [];
  currentAnswer.value = '';
  currentSources.value = [];
  error.value = '';
  loading.value = false;
};

const goToDocuments = () => {
  router.push(`/knowledge-bases/${knowledgeBaseId}/documents`);
};

const formatSource = (source: SourceItem) => {
  const truncated =
    source.content.length > 120 ? source.content.slice(0, 120) + '...' : source.content;
  return truncated;
};

const formatScore = (score: number) => {
  return (score * 100).toFixed(1) + '%';
};

const handleKeydown = (e: KeyboardEvent) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
};

onMounted(async () => {
  const detail = await getKnowledgeBaseDetail(knowledgeBaseId);
  if (detail.code === 0 && detail.data) {
    kbName.value = detail.data.name;
  }
});
</script>

<template>
  <section class="kb-doc-page chat-page">
    <header class="kb-doc-page__header chat-header">
      <div>
        <h2>{{ kbName || '知识库问答' }}</h2>
        <p>向知识库提问，AI 将基于文档内容回答。</p>
      </div>
      <div class="chat-header__actions">
        <el-button size="small" @click="newChat">新对话</el-button>
        <el-button size="small" @click="goToDocuments">返回文档列表</el-button>
      </div>
    </header>

    <div ref="messageListRef" class="chat-messages">
      <template v-for="(msg, idx) in messages" :key="idx">
        <div v-if="msg.role === 'user'" class="chat-msg chat-msg--user">
          <div class="chat-bubble chat-bubble--user">
            <p class="chat-bubble__text">{{ msg.content }}</p>
          </div>
        </div>

        <div v-else class="chat-msg chat-msg--assistant">
          <div class="chat-bubble chat-bubble--assistant">
            <div class="chat-bubble__markdown" v-html="mdRenderer(msg.content)" />
            <div v-if="msg.sources && msg.sources.length > 0" class="chat-sources">
              <div class="chat-sources__title">引用来源</div>
              <div v-for="(source, si) in msg.sources" :key="si" class="chat-source-card">
                <div class="chat-source-card__header">
                  <span class="chat-source-card__file">{{ source.filename }}</span>
                  <span class="chat-source-card__score">{{ formatScore(source.score) }}</span>
                </div>
                <p class="chat-source-card__preview">{{ formatSource(source) }}</p>
              </div>
            </div>
          </div>
        </div>
      </template>

      <div v-if="loading" class="chat-msg chat-msg--assistant">
        <div class="chat-bubble chat-bubble--assistant">
          <div
            v-if="currentAnswer"
            class="chat-bubble__markdown"
            v-html="mdRenderer(currentAnswer)"
          />
          <div v-else class="chat-loading">
            <span class="chat-loading__dot" />
            <span class="chat-loading__dot" />
            <span class="chat-loading__dot" />
          </div>
          <div v-if="currentSources.length > 0 && currentAnswer" class="chat-sources">
            <div class="chat-sources__title">引用来源</div>
            <div v-for="(source, si) in currentSources" :key="si" class="chat-source-card">
              <div class="chat-source-card__header">
                <span class="chat-source-card__file">{{ source.filename }}</span>
                <span class="chat-source-card__score">{{ formatScore(source.score) }}</span>
              </div>
              <p class="chat-source-card__preview">{{ formatSource(source) }}</p>
            </div>
          </div>
        </div>
      </div>

      <div v-if="error" class="chat-msg chat-msg--error">
        <div class="chat-bubble chat-bubble--error">
          <p>{{ error }}</p>
          <el-button size="small" type="primary" @click="retry">重试</el-button>
        </div>
      </div>
    </div>

    <div class="chat-input-area">
      <div class="chat-input__wrapper">
        <textarea
          v-model="inputText"
          class="chat-input"
          placeholder="输入你的问题..."
          :disabled="loading"
          @keydown="handleKeydown"
        />
        <el-button
          type="primary"
          :loading="loading"
          :disabled="!inputText.trim() || loading"
          @click="sendMessage"
        >
          发送
        </el-button>
      </div>
      <p class="chat-input__hint">Enter 发送，Shift + Enter 换行</p>
    </div>
  </section>
</template>

<style scoped>
.chat-page {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 160px);
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
  flex-shrink: 0;
}

.chat-header__actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px 0;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.chat-msg {
  display: flex;
}

.chat-msg--user {
  justify-content: flex-end;
}

.chat-msg--assistant {
  justify-content: flex-start;
}

.chat-msg--error {
  justify-content: center;
}

.chat-bubble {
  max-width: 75%;
  padding: 12px 16px;
  border-radius: 16px;
  line-height: 1.6;
  font-size: 14px;
}

.chat-bubble--user {
  background: #2563eb;
  color: #ffffff;
  border-bottom-right-radius: 4px;
}

.chat-bubble--assistant {
  background: #ffffff;
  border: 1px solid #dbe2ea;
  border-bottom-left-radius: 4px;
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.06);
}

.chat-bubble--error {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #991b1b;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.chat-bubble__text {
  margin: 0;
  white-space: pre-wrap;
  word-break: break-word;
}

.chat-bubble__markdown {
  word-break: break-word;
}

.chat-bubble__markdown :deep(p) {
  margin: 0 0 8px;
}

.chat-bubble__markdown :deep(p:last-child) {
  margin-bottom: 0;
}

.chat-bubble__markdown :deep(code) {
  background: #f1f5f9;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 13px;
}

.chat-bubble__markdown :deep(pre) {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 12px;
  overflow-x: auto;
  margin: 8px 0;
}

.chat-bubble__markdown :deep(pre code) {
  background: none;
  padding: 0;
}

.chat-bubble__markdown :deep(ul),
.chat-bubble__markdown :deep(ol) {
  padding-left: 20px;
  margin: 8px 0;
}

.chat-bubble__markdown :deep(blockquote) {
  border-left: 3px solid #2563eb;
  padding-left: 12px;
  margin: 8px 0;
  color: #64748b;
}

.chat-sources {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #e2e8f0;
}

.chat-sources__title {
  font-size: 12px;
  color: #94a3b8;
  margin-bottom: 8px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.chat-source-card {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 8px 12px;
  margin-bottom: 6px;
}

.chat-source-card:last-child {
  margin-bottom: 0;
}

.chat-source-card__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.chat-source-card__file {
  font-size: 12px;
  font-weight: 600;
  color: #2563eb;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 70%;
}

.chat-source-card__score {
  font-size: 11px;
  color: #64748b;
  flex-shrink: 0;
}

.chat-source-card__preview {
  font-size: 12px;
  color: #64748b;
  margin: 0;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.chat-loading {
  display: flex;
  gap: 4px;
  align-items: center;
  padding: 4px 0;
}

.chat-loading__dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #94a3b8;
  animation: chatPulse 1.4s ease-in-out infinite;
}

.chat-loading__dot:nth-child(2) {
  animation-delay: 0.2s;
}

.chat-loading__dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes chatPulse {
  0%,
  80%,
  100% {
    opacity: 0.3;
    transform: scale(0.8);
  }
  40% {
    opacity: 1;
    transform: scale(1);
  }
}

.chat-input-area {
  flex-shrink: 0;
  padding-top: 16px;
}

.chat-input__wrapper {
  display: flex;
  gap: 12px;
  align-items: flex-end;
}

.chat-input {
  flex: 1;
  min-height: 44px;
  max-height: 120px;
  padding: 10px 14px;
  border: 1px solid #dbe2ea;
  border-radius: 12px;
  font: inherit;
  font-size: 14px;
  line-height: 1.5;
  resize: none;
  outline: none;
  transition: border-color 0.2s ease;
}

.chat-input:focus {
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.chat-input:disabled {
  background: #f8fafc;
  cursor: not-allowed;
}

.chat-input__hint {
  margin-top: 6px;
  font-size: 12px;
  color: #94a3b8;
}
</style>
