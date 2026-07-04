<script setup lang="ts">
const summaryCards = [
  { label: '知识库总数', value: '3', note: '当前已创建并可管理的知识库' },
  { label: '文档总数', value: '44', note: '已进入知识库的文档资源数量' },
  { label: '处理中任务', value: '2', note: '等待解析或待更新的任务' },
]

const recentKnowledgeBases = [
  { name: '产品帮助中心', time: '今天 10:30 更新', status: '内容已同步' },
  { name: '面试题知识库', time: '今天 09:12 更新', status: '文档解析中' },
  { name: '项目规范文档', time: '昨天 18:45 更新', status: '等待补充材料' },
]

const todayTasks = [
  '检查"面试题知识库"的解析状态',
  '补充项目规范文档的最新版本',
  '准备 Day 3 的登录态和路由守卫改造',
]
</script>

<template>
  <section class="dashboard-page">
    <header class="dashboard-hero">
      <div>
        <p class="dashboard-hero__eyebrow">Workspace Overview</p>
        <h2>欢迎回来，今天继续把 AI 知识库项目往前推进。</h2>
        <p class="dashboard-hero__description">
          这是 Day 2 的工作台占位页版本，先把后台首页的信息结构搭稳，后面再逐步接入真实数据。
        </p>
      </div>
    </header>

    <div class="dashboard-summary">
      <el-card v-for="item in summaryCards" :key="item.label" shadow="hover">
        <div class="dashboard-card">
          <p class="dashboard-card__label">{{ item.label }}</p>
          <strong>{{ item.value }}</strong>
          <span>{{ item.note }}</span>
        </div>
      </el-card>
    </div>

    <div class="dashboard-panels">
      <el-card shadow="never">
        <template #header>
          <span>最近更新的知识库</span>
        </template>
        <ul class="dashboard-list">
          <li v-for="item in recentKnowledgeBases" :key="item.name" class="dashboard-list__item">
            <div>
              <strong>{{ item.name }}</strong>
              <p>{{ item.time }}</p>
            </div>
            <el-tag size="small">{{ item.status }}</el-tag>
          </li>
        </ul>
      </el-card>

      <el-card shadow="never">
        <template #header>
          <span>今日待处理</span>
        </template>
        <ul class="dashboard-todo">
          <li v-for="task in todayTasks" :key="task">{{ task }}</li>
        </ul>
      </el-card>
    </div>
  </section>
</template>
