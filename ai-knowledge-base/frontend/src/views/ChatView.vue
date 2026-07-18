<script setup lang="ts">
import { computed, nextTick, onMounted, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import MarkdownIt from 'markdown-it';
import {
  chatStream,
  deleteChatSession,
  getChatSessions,
  getKnowledgeBaseDetail,
  renameChatSession,
  saveChatSession,
  sendChatFeedback,
  type ChatSessionItem,
} from '../api/knowledge-bases';

import { sanitizeMarkdown } from '../utils/sanitize';

import EmptyState from '../components/EmptyState.vue';

const md = new MarkdownIt({ html: false, breaks: true });

const mdRenderer = (text: string) => sanitizeMarkdown(md.render(text));

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
  messageId?: number;
  feedback?: 'thumbs_up' | 'thumbs_down';
  feedbackComment?: string;
  showFeedbackComment?: boolean;
}

const route = useRoute();
const router = useRouter();
const knowledgeBaseId = route.params.id as string;
const kbName = ref('');
const documentCount = ref(0);

const sessions = ref<ChatSessionItem[]>([]);
const currentSessionId = ref<number | null>(null);
const messages = ref<Message[]>([]);
const inputText = ref('');
const loading = ref(false);
const loadingSessions = ref(false);
const currentAnswer = ref('');
const currentSources = ref<SourceItem[]>([]);
const error = ref('');
const abortController = ref<AbortController | null>(null);
const expandedKeys = ref<Set<string>>(new Set());

const messageListRef = ref<HTMLElement | null>(null);
const editingSessionId = ref<number | null>(null);
const editingTitle = ref('');
const editInputRef = ref<HTMLElement | null>(null);

const history = computed(() => messages.value.map((m) => ({ role: m.role, content: m.content })));

const parseTimestamp = (value?: string) => {
  if (!value) return Date.now();
  const parsed = new Date(value.replace(' ', 'T')).getTime();
  return Number.isNaN(parsed) ? Date.now() : parsed;
};

const mapMessages = (
  sessionMessages: {
    id?: number;
    role: 'user' | 'assistant';
    content: string;
    created_at?: string;
  }[],
) =>
  sessionMessages.map((msg) => ({
    messageId: msg.id,
    role: msg.role,
    content: msg.content,
    timestamp: parseTimestamp(msg.created_at),
  }));

const sortSessions = (items: ChatSessionItem[]) =>
  [...items].sort((a, b) => new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime());

const scrollToBottom = async () => {
  await nextTick();
  if (messageListRef.value) {
    messageListRef.value.scrollTop = messageListRef.value.scrollHeight;
  }
};

watch([messages, currentAnswer], scrollToBottom, { deep: true });

watch(editingSessionId, async (val) => {
  if (val !== null) {
    await nextTick();
    editInputRef.value?.focus();
  }
});

const setActiveSession = (session: ChatSessionItem | null) => {
  currentSessionId.value = session?.id ?? null;
  messages.value = session ? mapMessages(session.messages) : [];
  currentAnswer.value = '';
  currentSources.value = [];
  error.value = '';
};

const upsertSession = (session: ChatSessionItem) => {
  const next = sessions.value.filter((item) => item.id !== session.id);
  next.unshift(session);
  sessions.value = sortSessions(next);
};

const loadSessions = async () => {
  loadingSessions.value = true;
  try {
    const response = await getChatSessions(knowledgeBaseId);
    if (response.code === 0 && response.data) {
      sessions.value = sortSessions(response.data.items || []);
      setActiveSession(response.data.active_session);
    }
  } finally {
    loadingSessions.value = false;
  }
};

const persistCurrentSession = async (snapshot: Message[]) => {
  if (snapshot.length === 0) return;

  const response = await saveChatSession(Number(knowledgeBaseId), {
    session_id: currentSessionId.value,
    messages: snapshot.map((message) => ({
      role: message.role,
      content: message.content,
    })),
  });

  if (response.code === 0 && response.data) {
    currentSessionId.value = response.data.id;
    upsertSession(response.data);
    const apiMessages = response.data.messages || [];
    const updated = [...messages.value];
    let apiIdx = 0;
    for (let i = 0; i < updated.length && apiIdx < apiMessages.length; i++) {
      const u = updated[i]!;
      const a = apiMessages[apiIdx]!;
      if (u.role === a.role && u.content === a.content) {
        u.messageId = a.id;
        apiIdx++;
      }
    }
    messages.value = updated;
  }
};

const finalizeAnswer = async () => {
  const nextMessages = [
    ...messages.value,
    {
      role: 'assistant' as const,
      content: currentAnswer.value,
      sources: currentSources.value,
      timestamp: Date.now(),
    },
  ];

  messages.value = nextMessages;
  currentAnswer.value = '';
  currentSources.value = [];
  loading.value = false;
  abortController.value = null;

  try {
    await persistCurrentSession(nextMessages);
  } catch (err) {
    error.value = err instanceof Error ? err.message : '会话保存失败，请重试';
  }
};

const sendMessage = async () => {
  const text = inputText.value.trim();
  if (!text || loading.value) return;

  const requestHistory = history.value.slice();

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
    { query: text, history: requestHistory, top_k: 5 },
    {
      onToken: (token: string) => {
        currentAnswer.value += token;
      },
      onSources: (sources: SourceItem[]) => {
        currentSources.value = sources;
      },
      onDone: () => {
        void finalizeAnswer();
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
    const lastMsg = lastAssistantIdx >= 0 ? messages.value[lastAssistantIdx] : undefined;
    if (lastMsg && lastMsg.role === 'assistant') {
      messages.value.pop();
    }
  }
  error.value = '';
};

const requery = (msg: Message, idx: number) => {
  if (loading.value) return;
  messages.value = messages.value.slice(0, idx);
  inputText.value = msg.content;
  void sendMessage();
};

const newChat = () => {
  currentSessionId.value = null;
  messages.value = [];
  currentAnswer.value = '';
  currentSources.value = [];
  error.value = '';
  loading.value = false;
};

const deleteSession = async (session: ChatSessionItem) => {
  if (loading.value) return;
  try {
    await deleteChatSession(knowledgeBaseId, session.id);
    sessions.value = sessions.value.filter((s) => s.id !== session.id);
    if (currentSessionId.value === session.id) {
      if (sessions.value.length > 0) {
        setActiveSession(sessions.value[0] ?? null);
      } else {
        newChat();
      }
    }
  } catch {
    // ignore
  }
};

const startEditing = (session: ChatSessionItem) => {
  editingSessionId.value = session.id;
  editingTitle.value = session.title;
};

const saveTitle = async (session: ChatSessionItem) => {
  const title = editingTitle.value.trim();
  if (!title || title === session.title) {
    editingSessionId.value = null;
    return;
  }
  try {
    await renameChatSession(knowledgeBaseId, session.id, {
      messages: [{ role: 'user', content: title }],
    });
    session.title = title;
    sessions.value = sortSessions(sessions.value);
  } catch {
    // ignore
  }
  editingSessionId.value = null;
};

const selectSession = (session: ChatSessionItem) => {
  if (loading.value) return;
  setActiveSession(session);
};

const goToDocuments = () => {
  router.push(`/knowledge-bases/${knowledgeBaseId}/documents`);
};

const formatSource = (source: SourceItem) => {
  return source.content.length > 120 ? source.content.slice(0, 120) + '...' : source.content;
};

const formatScore = (score: number) => {
  return (score * 100).toFixed(1) + '%';
};

const submitFeedback = async (msg: Message, idx: number, feedback: 'thumbs_up' | 'thumbs_down') => {
  if (!msg.messageId) return;
  const updated = [...messages.value];
  const item = updated[idx];
  if (!item) return;
  updated[idx] = { ...item, feedback, showFeedbackComment: feedback === 'thumbs_down' };
  messages.value = updated;

  try {
    await sendChatFeedback(Number(knowledgeBaseId), {
      session_id: currentSessionId.value!,
      message_id: msg.messageId,
      feedback,
    });
  } catch {
    const reverted = [...messages.value];
    const revertedItem = reverted[idx];
    if (!revertedItem) return;
    reverted[idx] = { ...revertedItem, feedback: undefined, showFeedbackComment: false };
    messages.value = reverted;
  }
};

const submitFeedbackComment = async (msg: Message, idx: number) => {
  if (!msg.messageId || !msg.feedback) return;
  const comment = msg.feedbackComment?.trim() || '';
  try {
    await sendChatFeedback(Number(knowledgeBaseId), {
      session_id: currentSessionId.value!,
      message_id: msg.messageId,
      feedback: msg.feedback,
      comment,
    });
    const updated = [...messages.value];
    const item = updated[idx];
    if (!item) return;
    updated[idx] = { ...item, showFeedbackComment: false };
    messages.value = updated;
  } catch {
    // ignore
  }
};

const toggleSource = (key: string) => {
  const next = new Set(expandedKeys.value);
  if (next.has(key)) {
    next.delete(key);
  } else {
    next.add(key);
  }
  expandedKeys.value = next;
};

const formatTime = (ts: number) => {
  const now = Date.now();
  const diff = now - ts;
  if (diff < 60000) return '刚刚';
  if (diff < 3600000) return `${Math.floor(diff / 60000)} 分钟前`;
  const d = new Date(ts);
  const pad = (n: number) => String(n).padStart(2, '0');
  const hhmm = `${pad(d.getHours())}:${pad(d.getMinutes())}`;
  const today = new Date();
  if (d.toDateString() === today.toDateString()) return hhmm;
  if (d.getFullYear() === today.getFullYear()) {
    return `${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${hhmm}`;
  }
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${hhmm}`;
};

const formatSessionTime = (value: string) => {
  return formatTime(parseTimestamp(value));
};

const handleKeydown = (e: KeyboardEvent) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    void sendMessage();
  }
};

onMounted(async () => {
  const detail = await getKnowledgeBaseDetail(knowledgeBaseId);
  if (detail.code === 0 && detail.data) {
    kbName.value = detail.data.name;
    documentCount.value = detail.data.document_count;
  }
  await loadSessions();
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
        <el-button size="small" @click="router.push(`/knowledge-bases/${knowledgeBaseId}/compare`)"
          >效果对比</el-button
        >
        <el-button size="small" @click="goToDocuments">返回文档列表</el-button>
      </div>
    </header>

    <div class="chat-layout">
      <aside class="chat-sidebar">
        <div class="chat-sidebar__header">
          <h3>会话历史</h3>
          <el-button size="small" text @click="newChat">新建</el-button>
        </div>
        <div v-if="loadingSessions" class="chat-sidebar__empty">加载中...</div>
        <EmptyState
          v-else-if="sessions.length === 0"
          title="暂无历史会话"
          description="新建一个会话开始提问吧"
        />
        <div
          v-for="session in sessions"
          :key="session.id"
          class="chat-session-item"
          :class="{ 'chat-session-item--active': currentSessionId === session.id }"
        >
          <div
            class="chat-session-item__main"
            :class="{ 'chat-session-item__main--disabled': loading }"
            @click="selectSession(session)"
          >
            <span
              v-if="editingSessionId !== session.id"
              class="chat-session-item__title"
              @dblclick.stop="startEditing(session)"
            >
              {{ session.title }}
            </span>
            <input
              v-else
              v-model="editingTitle"
              class="chat-session-item__edit-input"
              @keydown.enter="saveTitle(session)"
              @keydown.escape="editingSessionId = null"
              @blur="saveTitle(session)"
              @click.stop
              ref="editInputRef"
            />
            <span class="chat-session-item__time">{{ formatSessionTime(session.updated_at) }}</span>
          </div>
          <button
            class="chat-session-item__delete"
            :disabled="loading"
            @click.stop="deleteSession(session)"
            title="删除会话"
          >
            ×
          </button>
        </div>
      </aside>

      <div class="chat-main">
        <div ref="messageListRef" class="chat-messages">
          <div v-if="documentCount === 0 && messages.length === 0" class="chat-empty-alert">
            该知识库暂无文档，请先<a
              class="chat-empty-alert__link"
              :href="`/knowledge-bases/${knowledgeBaseId}/documents`"
              >上传文档</a
            >后再提问。
          </div>
          <div v-else-if="messages.length === 0 && !loading" class="chat-empty-state">
            新建会话后发送第一条消息，系统会在回答完成后自动保存会话。
          </div>

          <template v-for="(msg, idx) in messages" :key="idx">
            <div v-if="msg.role === 'user'" class="chat-msg chat-msg--user">
              <div class="chat-msg__body chat-msg__body--user">
                <div class="chat-bubble chat-bubble--user">
                  <p class="chat-bubble__text">{{ msg.content }}</p>
                  <el-button
                    size="small"
                    text
                    class="chat-requery-btn"
                    :disabled="loading"
                    @click="requery(msg, idx)"
                  >
                    重新提问
                  </el-button>
                </div>
                <p class="chat-timestamp">{{ formatTime(msg.timestamp) }}</p>
              </div>
            </div>

            <div v-else class="chat-msg chat-msg--assistant">
              <div class="chat-msg__body chat-msg__body--assistant">
                <div class="chat-bubble chat-bubble--assistant">
                  <div class="chat-bubble__markdown" v-html="mdRenderer(msg.content)" />
                  <div v-if="msg.sources" class="chat-sources">
                    <div class="chat-sources__title">引用来源</div>
                    <template v-if="msg.sources.length > 0">
                      <div v-for="(source, si) in msg.sources" :key="si" class="chat-source-card">
                        <div class="chat-source-card__header">
                          <span class="chat-source-card__file">{{ source.filename }}</span>
                          <span class="chat-source-card__score">{{
                            formatScore(source.score)
                          }}</span>
                        </div>
                        <p class="chat-source-card__preview">
                          {{
                            expandedKeys.has(`msg-${idx}-${si}`)
                              ? source.content
                              : formatSource(source)
                          }}
                        </p>
                        <button
                          v-if="source.content.length > 120"
                          class="chat-source-card__expand"
                          @click="toggleSource(`msg-${idx}-${si}`)"
                        >
                          {{ expandedKeys.has(`msg-${idx}-${si}`) ? '收起' : '展开完整内容' }}
                        </button>
                      </div>
                    </template>
                    <p v-else class="chat-no-sources">
                      未在知识库中找到与问题相关的文档内容，AI 回答可能不准确。
                    </p>
                  </div>
                  <div v-if="msg.messageId" class="chat-feedback">
                    <button
                      class="chat-feedback__btn"
                      :class="{ 'chat-feedback__btn--active': msg.feedback === 'thumbs_up' }"
                      :disabled="loading"
                      @click="submitFeedback(msg, idx, 'thumbs_up')"
                    >
                      👍
                    </button>
                    <button
                      class="chat-feedback__btn"
                      :class="{ 'chat-feedback__btn--active': msg.feedback === 'thumbs_down' }"
                      :disabled="loading"
                      @click="submitFeedback(msg, idx, 'thumbs_down')"
                    >
                      👎
                    </button>
                    <textarea
                      v-if="msg.showFeedbackComment"
                      v-model="msg.feedbackComment"
                      class="chat-feedback__comment"
                      placeholder="请输入反馈备注（可选）"
                      rows="2"
                    />
                    <button
                      v-if="msg.showFeedbackComment"
                      class="chat-feedback__submit"
                      @click="submitFeedbackComment(msg, idx)"
                    >
                      提交
                    </button>
                  </div>
                </div>
                <p class="chat-timestamp">{{ formatTime(msg.timestamp) }}</p>
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
                  <p class="chat-source-card__preview">
                    {{ expandedKeys.has(`loading-${si}`) ? source.content : formatSource(source) }}
                  </p>
                  <button
                    v-if="source.content.length > 120"
                    class="chat-source-card__expand"
                    @click="toggleSource(`loading-${si}`)"
                  >
                    {{ expandedKeys.has(`loading-${si}`) ? '收起' : '展开完整内容' }}
                  </button>
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
      </div>
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

.chat-layout {
  flex: 1;
  min-height: 0;
  display: grid;
  grid-template-columns: 240px minmax(0, 1fr);
  gap: 16px;
}

.chat-sidebar {
  min-height: 0;
  display: flex;
  flex-direction: column;
  border: 1px solid #dbe2ea;
  border-radius: 8px;
  background: #ffffff;
  overflow: hidden;
}

.chat-sidebar__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  border-bottom: 1px solid #e2e8f0;
}

.chat-sidebar__header h3 {
  margin: 0;
  font-size: 14px;
}

.chat-sidebar__empty {
  padding: 16px 12px;
  color: #64748b;
  font-size: 13px;
}

.chat-session-item {
  display: flex;
  align-items: stretch;
  width: 100%;
  border-bottom: 1px solid #f1f5f9;
  background: #ffffff;
}

.chat-session-item:hover {
  background: #f8fafc;
}

.chat-session-item:hover .chat-session-item__delete {
  display: flex;
}

.chat-session-item--active {
  background: #eff6ff;
}

.chat-session-item__main {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 4px;
  padding: 12px;
  cursor: pointer;
  min-width: 0;
}

.chat-session-item__main--disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.chat-session-item__title {
  width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 13px;
  color: #0f172a;
}

.chat-session-item__edit-input {
  width: 100%;
  font-size: 13px;
  padding: 2px 4px;
  border: 1px solid #409eff;
  border-radius: 4px;
  outline: none;
  background: #ffffff;
  color: #0f172a;
}

.chat-session-item__time {
  font-size: 11px;
  color: #94a3b8;
}

.chat-session-item__delete {
  display: none;
  align-items: center;
  justify-content: center;
  width: 32px;
  border: 0;
  background: transparent;
  color: #94a3b8;
  font-size: 18px;
  cursor: pointer;
  flex-shrink: 0;
}

.chat-session-item__delete:hover {
  color: #ef4444;
  background: #fef2f2;
}

.chat-main {
  min-height: 0;
  display: flex;
  flex-direction: column;
}

.chat-messages {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding: 16px 0;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.chat-empty-state {
  color: #64748b;
  font-size: 14px;
  padding: 24px 0;
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
  padding: 12px 16px;
  border-radius: 16px;
  line-height: 1.6;
  font-size: 14px;
}

.chat-msg__body {
  display: flex;
  flex-direction: column;
  max-width: 75%;
}

.chat-msg__body--user {
  align-items: flex-end;
}

.chat-msg__body--assistant {
  align-items: flex-start;
}

.chat-timestamp {
  font-size: 11px;
  color: #94a3b8;
  margin: 4px 8px 0;
  flex-shrink: 0;
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

.chat-requery-btn {
  margin-top: 6px;
  padding: 0;
  color: rgba(255, 255, 255, 0.7);
  font-size: 12px;
}

.chat-requery-btn:hover {
  color: #ffffff;
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
  gap: 12px;
  margin-bottom: 4px;
}

.chat-source-card__file,
.chat-source-card__preview {
  word-break: break-word;
}

.chat-source-card__file {
  font-size: 13px;
  font-weight: 600;
  color: #0f172a;
}

.chat-source-card__score {
  font-size: 12px;
  color: #2563eb;
}

.chat-source-card__preview {
  margin: 0;
  color: #475569;
  font-size: 13px;
  line-height: 1.5;
}

.chat-source-card__expand {
  margin-top: 6px;
  border: 0;
  background: transparent;
  color: #2563eb;
  font-size: 12px;
  cursor: pointer;
  padding: 0;
}

.chat-no-sources {
  margin: 0;
  color: #64748b;
  font-size: 13px;
}

.chat-loading {
  display: flex;
  align-items: center;
  gap: 6px;
  min-height: 20px;
}

.chat-loading__dot {
  width: 8px;
  height: 8px;
  border-radius: 999px;
  background: #94a3b8;
  animation: chat-blink 1.2s infinite ease-in-out;
}

.chat-loading__dot:nth-child(2) {
  animation-delay: 0.15s;
}

.chat-loading__dot:nth-child(3) {
  animation-delay: 0.3s;
}

.chat-input-area {
  flex-shrink: 0;
  padding-top: 12px;
}

.chat-input__wrapper {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 12px;
  align-items: flex-end;
}

.chat-input {
  width: 100%;
  min-height: 104px;
  resize: vertical;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 12px 14px;
  font-size: 14px;
  line-height: 1.6;
  font-family: inherit;
  color: #0f172a;
  outline: none;
}

.chat-input:focus {
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
}

.chat-input__hint {
  margin: 8px 2px 0;
  font-size: 12px;
  color: #94a3b8;
}

.chat-empty-alert {
  padding: 16px;
  border-radius: 8px;
  background: #fff7ed;
  color: #9a3412;
  font-size: 14px;
}

.chat-empty-alert__link {
  color: #c2410c;
  font-weight: 600;
}

.chat-feedback {
  display: flex;
  align-items: flex-start;
  gap: 6px;
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px solid #e2e8f0;
  flex-wrap: wrap;
}

.chat-feedback__btn {
  border: 1px solid #dbe2ea;
  background: #f8fafc;
  border-radius: 6px;
  padding: 2px 8px;
  font-size: 14px;
  cursor: pointer;
  line-height: 1.6;
  transition: all 0.15s;
}

.chat-feedback__btn:hover {
  background: #eff6ff;
  border-color: #2563eb;
}

.chat-feedback__btn--active {
  background: #eff6ff;
  border-color: #2563eb;
  box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.15);
}

.chat-feedback__comment {
  width: 100%;
  border: 1px solid #dbe2ea;
  border-radius: 6px;
  padding: 6px 8px;
  font-size: 13px;
  font-family: inherit;
  outline: none;
  resize: vertical;
  margin-top: 4px;
}

.chat-feedback__comment:focus {
  border-color: #2563eb;
}

.chat-feedback__submit {
  border: 0;
  background: #2563eb;
  color: #ffffff;
  border-radius: 6px;
  padding: 4px 12px;
  font-size: 12px;
  cursor: pointer;
}

.chat-feedback__submit:hover {
  background: #1d4ed8;
}

@keyframes chat-blink {
  0%,
  80%,
  100% {
    opacity: 0.3;
  }
  40% {
    opacity: 1;
  }
}
</style>
