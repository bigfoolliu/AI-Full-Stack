<script setup lang="ts">
import { reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import type { FormInstance, FormRules } from 'element-plus';
import { createKnowledgeBase } from '../api/knowledge-bases';

const router = useRouter();

const formRef = ref<FormInstance>();

const form = reactive({
  name: '',
  description: '',
});

const rules: FormRules = {
  name: [
    { required: true, message: '知识库名称不能为空', trigger: 'blur' },
    { min: 1, max: 50, message: '名称长度为 1-50 个字符', trigger: 'blur' },
    {
      validator: (_rule: unknown, value: string, callback: (error?: Error) => void) => {
        if (value && !value.trim()) {
          callback(new Error('名称不能只包含空格'));
        } else {
          callback();
        }
      },
      trigger: 'blur',
    },
  ],
  description: [{ max: 200, message: '描述不超过 200 个字符', trigger: 'blur' }],
};

const loading = ref(false);

const goBack = () => {
  router.push('/knowledge-bases');
};

const handleSubmit = async () => {
  if (!formRef.value) return;

  const valid = await formRef.value.validate().catch(() => false);
  if (!valid) return;

  loading.value = true;

  try {
    const result = await createKnowledgeBase({
      name: form.name.trim(),
      description: form.description.trim(),
    });

    if (result.code !== 0 || !result.data) {
      ElMessage.error(result.message || '创建知识库失败');
      return;
    }

    ElMessage.success(`知识库“${result.data.name}”创建成功`);
    router.push(`/knowledge-bases/${result.data.id}/documents`);
  } catch {
    ElMessage.error('创建知识库请求失败，请稍后重试');
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
      <el-form ref="formRef" :model="form" :rules="rules" label-position="top">
        <el-form-item label="知识库名称" prop="name">
          <el-input v-model="form.name" placeholder="例如：产品知识库" maxlength="50" />
        </el-form-item>
        <el-form-item label="知识库描述" prop="description">
          <el-input
            v-model="form.description"
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
          {{ loading ? '创建中...' : '创建知识库' }}
        </el-button>
      </div>
    </el-card>
  </section>
</template>
