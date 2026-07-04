<script setup lang="ts">
import { ref } from "vue";
import { useRoute } from "vue-router";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import { UploadFilled } from "@element-plus/icons-vue";

const route = useRoute();
const router = useRouter();

const selectedFileName = ref("");

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  const file = target.files?.[0];
  selectedFileName.value = file?.name ?? "";
};

const goBack = () => {
  router.push(`/knowledge-bases/${route.params.id}/documents`);
};

const handleUpload = () => {
  if (!selectedFileName.value) {
    ElMessage.warning("请先选择一个要上传的文档");
    return;
  }

  ElMessage.success("文档上传入口已触发（当前为前端占位版本，后续将接入真实上传接口）");
};
</script>

<template>
  <section class="kb-upload-page">
    <header class="kb-upload-page__header">
      <h2>文档上传页</h2>
      <p>当前知识库 ID：{{ route.params.id }}</p>
      <p>先把文档上传入口和页面交互搭出来，后续再接入真实文件上传与解析流程。</p>
    </header>

    <el-card class="kb-upload-card">
      <el-upload
        drag
        action=""
        :auto-upload="false"
        :show-file-list="true"
        @change="handleFileChange"
      >
        <el-icon class="el-icon--upload" :size="40">
          <UploadFilled />
        </el-icon>
        <div class="el-upload__text">
          将文件拖拽到此处，或 <em>点击选择文件</em>
        </div>
      </el-upload>

      <div class="kb-form-actions" style="margin-top: 20px">
        <el-button @click="goBack">返回文档列表</el-button>
        <el-button type="primary" @click="handleUpload">上传文档</el-button>
      </div>
    </el-card>
  </section>
</template>
