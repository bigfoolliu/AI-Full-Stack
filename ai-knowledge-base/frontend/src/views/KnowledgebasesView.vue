<script setup lang="ts">
const knowledgeBases = [
  {
    id: 1,
    name: '产品帮助中心',
    documents: 24,
    status: '已启用',
    updatedAt: '2026-06-28 10:30',
  },
  {
    id: 2,
    name: '面试题知识库',
    documents: 12,
    status: '解析中',
    updatedAt: '2026-06-28 09:12',
  },
  {
    id: 3,
    name: '项目规范文档',
    documents: 8,
    status: '待更新',
    updatedAt: '2026-06-27 18:45',
  },
]

const getStatusClass = (status: string) => {
  if (status === '已启用') return 'kb-status--success'
  if (status === '解析中') return 'kb-status--processing'
  return 'kb-status--warning'
}
</script>

<template>
  <section class="kb-page">
    <header class="kb-page__header">
      <div>
        <h2>知识库列表</h2>
        <p>集中管理你的文档知识库，后续这里会接入真实搜索、上传和状态流转能力。</p>
      </div>
    </header>

    <div class="kb-toolbar">
      <input class="kb-search" type="text" placeholder="搜索知识库名称" />
      <button type="button" class="kb-create-button">新建知识库</button>
    </div>

    <div class="kb-table-card">
      <table class="kb-table">
        <thead>
          <tr>
            <th>知识库名称</th>
            <th>文档数</th>
            <th>状态</th>
            <th>更新时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in knowledgeBases" :key="item.id">
            <td>
              <div class="kb-name-cell">
                <strong>{{ item.name }}</strong>
                <span>用于 AI 对话检索的资料集合</span>
              </div>
            </td>
            <td>{{ item.documents }}</td>
            <td>
              <span class="kb-status" :class="getStatusClass(item.status)">
                {{ item.status }}
              </span>
            </td>
            <td>{{ item.updatedAt }}</td>
            <td>
              <div class="kb-actions">
                <button type="button">查看</button>
                <button type="button">编辑</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <p class="kb-page__hint">当前列表使用前端占位数据，Day 4 接口完成后会替换为真实返回结果。</p>
  </section>
</template>
