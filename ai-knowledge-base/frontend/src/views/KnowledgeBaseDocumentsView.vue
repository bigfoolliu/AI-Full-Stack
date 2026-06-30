<script setup lang="ts">
import { useRoute } from "vue-router";
import { useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();

const knowledgeBaseId = route.params.id;

const documents = [
  {
    id: 1,
    name: "产品介绍.pdf",
    status: "已完成",
    updatedAt: "2026-07-01 09:30",
  },
  {
    id: 2,
    name: "FAQ_v2.docx",
    status: "解析中",
    updatedAt: "2026-07-01 10:05",
  },
  {
    id: 3,
    name: "售后流程说明.txt",
    status: "待处理",
    updatedAt: "2026-06-30 18:20",
  },
];

const goBack = () => {
  router.push("/knowledge-bases");
};

const goToUpload = () => {
  router.push(`/knowledge-bases/${knowledgeBaseId}/upload`);
};

const getStatusClass = (status: string) => {
  if (status === "已完成") return "kb-doc-status--success";
  if (status === "解析中") return "kb-doc-status--processing";
  return "kb-doc-status--pending";
};
</script>

<template>
  <section class="kb-doc-page">
    <header class="kb-doc-page__header">
      <div>
        <h2>文档列表 / 状态页</h2>
        <p>查看当前知识库下的文档处理情况，并继续推进上传与解析流程。</p>
      </div>
    </header>

    <div class="kb-doc-context">
      <strong>当前知识库 ID：{{ route.params.id }}</strong>
      <p>这里后续会继续补充当前知识库名称、说明和统计信息。</p>
    </div>

    <div class="kb-doc-actions">
      <button type="button" class="kb-secondary-button" @click="goBack">
        返回知识库列表
      </button>
      <button type="button" class="kb-primary-button" @click="goToUpload">
        去上传文档
      </button>
    </div>

    <div class="kb-doc-table-card">
      <table class="kb-doc-table">
        <thead>
          <tr>
            <th>文档名称</th>
            <th>状态</th>
            <th>更新时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in documents" :key="item.id">
            <td>{{ item.name }}</td>
            <td>
              <span class="kb-doc-status" :class="getStatusClass(item.status)">
                {{ item.status }}
              </span>
            </td>
            <td>{{ item.updatedAt }}</td>
            <td>
              <div class="kb-actions">
                <button type="button">查看</button>
                <button type="button">重试</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>
