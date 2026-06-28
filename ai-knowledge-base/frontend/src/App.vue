<script setup lang="ts">
</script>

<template>
  <h1>Hello App!</h1>
  <p>
    <strong>Current route path:</strong> {{ $route.fullPath }}
  </p>
  <nav>
    <div>
      <RouterLink to="/">Go to Home</RouterLink>
    </div>
    <div>
      <RouterLink to="/about">Go to About</RouterLink>
    </div>
  </nav>
  <main>
    <RouterView />
  </main>
</template>
