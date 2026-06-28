import { computed, ref } from "vue";
import { defineStore } from "pinia";

const STORAGE_TOKEN_KEY = "ai-kb-token";
const STORAGE_USERNAME_KEY = "ai-kb-username";

export const useUserStore = defineStore("user", () => {
  const token = ref("");
  const username = ref("");

  const isLoggedIn = computed(() => Boolean(token.value));

  const persist = () => {
    localStorage.setItem(STORAGE_TOKEN_KEY, token.value);
    localStorage.setItem(STORAGE_USERNAME_KEY, username.value);
  };

  const clearPersisted = () => {
    localStorage.removeItem(STORAGE_TOKEN_KEY);
    localStorage.removeItem(STORAGE_USERNAME_KEY);
  };

  const restore = () => {
    token.value = localStorage.getItem(STORAGE_TOKEN_KEY) ?? "";
    username.value = localStorage.getItem(STORAGE_USERNAME_KEY) ?? "";
  };

  // 登陆
  const login = (nextUsername: string) => {
    token.value = `mock-token-${Date.now()}`;
    username.value = nextUsername;
    persist();
  };

  // 登出
  const logout = () => {
    token.value = "";
    username.value = "";
    clearPersisted();
  };

  return {
    token,
    username,
    isLoggedIn,
    restore,
    login,
    logout,
  };
});
