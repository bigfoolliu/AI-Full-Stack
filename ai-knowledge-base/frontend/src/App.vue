<script setup lang="ts">
</script>

<template>
  <div>
    <router-link to="/">首页</router-link>
  </div>
  <div>
    <router-link to="/about">关于</router-link>
  </div>
  <div>
    <router-link to="/login">登录</router-link>
  </div>
  <div>
    <router-link to="/dashboard">面板</router-link>
  </div>
  <div>
    <router-link to="/knowledge-bases">知识库</router-link>
  </div>


  <div>
    <RouterView />
  </div>
</template>
