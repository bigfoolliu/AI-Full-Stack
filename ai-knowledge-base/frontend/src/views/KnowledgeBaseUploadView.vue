<script setup lang="ts">
import { ref } from 'vue';
import { useRoute } from 'vue-router';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import { UploadFilled } from '@element-plus/icons-vue';
import type { UploadInstance, UploadRawFile } from 'element-plus';
import { getUploadUrl, getUploadHeaders } from '../api/knowledge-bases';

const route = useRoute();
const router = useRouter();

const uploadRef = ref<UploadInstance>();
const loading = ref(false);

const knowledgeBaseId = route.params.id;
const uploadUrl = getUploadUrl(String(knowledgeBaseId));
const uploadHeaders = getUploadHeaders();

const goBack = () => {
  router.push(`/knowledge-bases/${knowledgeBaseId}/documents`);
};

const beforeUpload = (rawFile: UploadRawFile) => {
  const maxSize = 50 * 1024 * 1024;
  if (rawFile.size > maxSize) {
    ElMessage.error('文件大小不能超过 50MB');
    return false;
  }
  loading.value = true;
  return true;
};

const onSuccess = () => {
  loading.value = false;
  ElMessage.success('文件上传成功');
  router.push(`/knowledge-bases/${knowledgeBaseId}/documents`);
};

const onError = () => {
  loading.value = false;
  ElMessage.error('上传失败，请重试');
};
</script>

<template>
  <section class="kb-upload-page">
    <header class="kb-upload-page__header">
      <h2>文档上传</h2>
      <p>为知识库 ID：{{ knowledgeBaseId }} 上传文档</p>
    </header>

    <el-card class="kb-upload-card">
      <el-upload
        ref="uploadRef"
        :action="uploadUrl"
        :headers="uploadHeaders"
        :auto-upload="true"
        drag
        :show-file-list="true"
        :before-upload="beforeUpload"
        :on-success="onSuccess"
        :on-error="onError"
      >
        <el-icon class="el-icon--upload" :size="40">
          <UploadFilled />
        </el-icon>
        <div class="el-upload__text">将文件拖拽到此处，或 <em>点击选择文件</em></div>
        <template #tip>
          <div style="color: #909399; font-size: 13px; margin-top: 4px">
            支持 PDF、Word、TXT 等常见文档格式，单个文件不超过 50MB。
          </div>
        </template>
      </el-upload>

      <div class="kb-form-actions" style="margin-top: 20px">
        <el-button :disabled="loading" @click="goBack">返回文档列表</el-button>
      </div>
    </el-card>
  </section>
</template>
