<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

const name = ref("");
const description = ref("");
const errorMessage = ref("");
const successMessage = ref("");

const goBack = () => {
  router.push("/knowledge-bases");
};

const handleSubmit = () => {
  errorMessage.value = "";
  successMessage.value = "";

  if (!name.value.trim()) {
    errorMessage.value = "知识库名称不能为空";
    return;
  }

  successMessage.value = "知识库表单已提交（当前为前端占位版本，后续将接入真实创建接口）";
};
</script>

<template>
  <section class="kb-form-page">
    <header class="kb-form-page__header">
      <h2>新建知识库</h2>
      <p>先把知识库创建页的表单结构搭出来，后续再接入真实创建接口与创建成功后的流转。</p>
    </header>

    <div class="kb-form-card">
      <div class="kb-form-card__body">
        <label class="kb-form-field">
          <span>知识库名称</span>
          <input v-model="name" type="text" placeholder="例如：产品知识库" maxlength="50" />
        </label>

        <label class="kb-form-field">
          <span>知识库描述</span>
          <textarea v-model="description" rows="5" placeholder="简单描述这个知识库的用途、资料范围或目标用户" maxlength="200" />
        </label>

        <p v-if="errorMessage" class="kb-form-message kb-form-message--error">
          {{ errorMessage }}
        </p>

        <p v-if="successMessage" class="kb-form-message kb-form-message--success">
          {{ successMessage }}
        </p>
      </div>

      <div class="kb-form-actions">
        <button type="button" class="kb-secondary-button" @click="goBack">
          返回列表
        </button>
        <button type="button" class="kb-primary-button" @click="handleSubmit">
          创建知识库
        </button>
      </div>
    </div>
  </section>
</template>
