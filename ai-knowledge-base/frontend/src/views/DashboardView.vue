<script setup lang="ts">
const summaryCards = [
  { title: '知识库总数', value: 3 },
  { title: '文档总数', value: 44 },
  { title: '处理中任务', value: 2 },
];

const recentKnowledgeBases = [
  { name: '产品帮助中心', time: '今天 10:30 更新', status: '内容已同步', statusType: 'success' },
  { name: '面试题知识库', time: '今天 09:12 更新', status: '文档解析中', statusType: 'warning' },
  { name: '项目规范文档', time: '昨天 18:45 更新', status: '等待补充材料', statusType: 'info' },
];

const todayTasks = [
  '检查"面试题知识库"的解析状态',
  '补充项目规范文档的最新版本',
  '添加搜索/筛选功能的知识库列表验证',
];
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
      <el-card v-for="item in summaryCards" :key="item.title" shadow="hover">
        <el-statistic :value="item.value" :title="item.title" />
      </el-card>
    </div>

    <div class="dashboard-panels">
      <el-card shadow="never">
        <template #header>
          <span>最近更新的知识库</span>
        </template>
        <div v-for="item in recentKnowledgeBases" :key="item.name" class="dashboard-list-item">
          <div>
            <strong>{{ item.name }}</strong>
            <p>{{ item.time }}</p>
          </div>
          <el-tag :type="item.statusType as any" size="small">{{ item.status }}</el-tag>
        </div>
      </el-card>

      <el-card shadow="never">
        <template #header>
          <span>今日待处理</span>
        </template>
        <div v-for="task in todayTasks" :key="task" class="dashboard-todo-item">
          {{ task }}
        </div>
      </el-card>
    </div>
  </section>
</template>
