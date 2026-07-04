<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import { createKnowledgeBase } from "../api/knowledge-bases";

const router = useRouter();

const name = ref("");
const description = ref("");
const loading = ref(false);

const goBack = () => {
  router.push("/knowledge-bases");
};

const handleSubmit = async () => {
  if (!name.value.trim()) {
    ElMessage.warning("知识库名称不能为空");
    return;
  }

  loading.value = true;

  try {
    const result = await createKnowledgeBase({
      name: name.value.trim(),
      description: description.value.trim(),
    });

    if (result.code !== 0 || !result.data) {
      ElMessage.error(result.message || "创建知识库失败");
      return;
    }

    ElMessage.success(`知识库“${result.data.name}”创建成功`);
    router.push("/knowledge-bases");
  } catch {
    ElMessage.error("创建知识库请求失败，请稍后重试");
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <section class="kb-form-page">
    <header class="kb-form-page__header">
      <h2>新建知识库</h2>
      <p>创建一个新的知识库来管理文档资料。</p>
    </header>

    <el-card class="kb-form-card">
      <el-form label-width="100" label-position="top">
        <el-form-item label="知识库名称" required>
          <el-input v-model="name" placeholder="例如：产品知识库" maxlength="50" />
        </el-form-item>
        <el-form-item label="知识库描述">
          <el-input
            v-model="description"
            type="textarea"
            :rows="5"
            placeholder="简单描述这个知识库的用途、资料范围或目标用户"
            maxlength="200"
            show-word-limit
          />
        </el-form-item>
      </el-form>

      <div class="kb-form-actions">
        <el-button @click="goBack">返回列表</el-button>
        <el-button type="primary" :loading="loading" @click="handleSubmit">
          {{ loading ? "创建中..." : "创建知识库" }}
        </el-button>
      </div>
    </el-card>
  </section>
</template>
