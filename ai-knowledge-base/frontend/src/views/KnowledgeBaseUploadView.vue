<script setup lang="ts">
import { ref } from "vue";
import { useRoute } from "vue-router";
import { useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();

const selectedFileName = ref("");
const errorMessage = ref("");
const successMessage = ref("");

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  const file = target.files?.[0];

  selectedFileName.value = file?.name ?? "";
  errorMessage.value = "";
  successMessage.value = "";
};

const goBack = () => {
  router.push(`/knowledge-bases/${route.params.id}/documents`);
};

const handleUpload = () => {
  errorMessage.value = "";
  successMessage.value = "";

  if (!selectedFileName.value) {
    errorMessage.value = "请先选择一个要上传的文档";
    return;
  }

  successMessage.value =
    "文档上传入口已触发（当前为前端占位版本，后续将接入真实上传接口）";
};
</script>

<template>
  <section class="kb-upload-page">
    <header class="kb-upload-page__header">
      <h2>文档上传页</h2>
      <p>当前知识库 ID：{{ route.params.id }}</p>
      <p>先把文档上传入口和页面交互搭出来，后续再接入真实文件上传与解析流程。</p>
    </header>

    <div class="kb-upload-card">
      <label class="kb-upload-field">
        <span>选择文档</span>
        <input type="file" @change="handleFileChange" />
      </label>

      <p class="kb-upload-file" v-if="selectedFileName">
        当前选择：{{ selectedFileName }}
      </p>

      <p v-if="errorMessage" class="kb-form-message kb-form-message--error">
        {{ errorMessage }}
      </p>

      <p v-if="successMessage" class="kb-form-message kb-form-message--success">
        {{ successMessage }}
      </p>

      <div class="kb-form-actions">
        <button type="button" class="kb-secondary-button" @click="goBack">
          返回文档列表
        </button>
        <button type="button" class="kb-primary-button" @click="handleUpload">
          上传文档
        </button>
      </div>
    </div>
  </section>
</template>
