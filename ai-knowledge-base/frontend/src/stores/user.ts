import { computed, ref } from "vue";
import { defineStore } from "pinia";
import { getMe, login as loginRequest } from "../api/auth";

const STORAGE_TOKEN_KEY = "ai-kb-token";
const STORAGE_USERNAME_KEY = "ai-kb-username";
const STORAGE_NICKNAME_KEY = "ai-kb-nickname";

export const useUserStore = defineStore("user", () => {
  const token = ref("");
  const username = ref("");
  const nickname = ref("");
  const loginLoading = ref(false);
  const loginError = ref("");

  const isLoggedIn = computed(() => Boolean(token.value));

  const persist = () => {
    localStorage.setItem(STORAGE_TOKEN_KEY, token.value);
    localStorage.setItem(STORAGE_USERNAME_KEY, username.value);
    localStorage.setItem(STORAGE_NICKNAME_KEY, nickname.value);
  };

  const clearPersisted = () => {
    localStorage.removeItem(STORAGE_TOKEN_KEY);
    localStorage.removeItem(STORAGE_USERNAME_KEY);
    localStorage.removeItem(STORAGE_NICKNAME_KEY);
  };

  const restore = () => {
    token.value = localStorage.getItem(STORAGE_TOKEN_KEY) ?? "";
    username.value = localStorage.getItem(STORAGE_USERNAME_KEY) ?? "";
    nickname.value = localStorage.getItem(STORAGE_NICKNAME_KEY) ?? "";
  };

  const login = async (nextUsername: string, password: string) => {
    loginLoading.value = true;
    loginError.value = "";

    try {
      const result = await loginRequest({
        username: nextUsername,
        password,
      });

      if (result.code !== 0 || !result.data) {
        loginError.value = result.message || "登录失败";
        return false;
      }

      token.value = result.data.token;
      username.value = result.data.user.username;
      nickname.value = result.data.user.nickname;
      persist();
      return true;
    } catch (error: unknown) {
      const axiosErr = error as { response?: { data?: Record<string, unknown> } } | null;
      loginError.value = (axiosErr?.response?.data?.detail as string) || "登录请求失败，请稍后重试";
      return false;
    } finally {
      loginLoading.value = false;
    }
  };

  const fetchMe = async () => {
    if (!token.value) {
      return false;
    }

    try {
      const result = await getMe();

      if (result.code !== 0 || !result.data) {
        logout();
        return false;
      }

      username.value = result.data.username;
      nickname.value = result.data.nickname;
      persist();
      return true;
    } catch {
      logout();
      return false;
    }
  };

  const clearError = () => {
    loginError.value = "";
  };

  const logout = () => {
    token.value = "";
    username.value = "";
    nickname.value = "";
    loginError.value = "";
    clearPersisted();
  };

  return {
    token,
    username,
    nickname,
    isLoggedIn,
    loginLoading,
    loginError,
    restore,
    fetchMe,
    clearError,
    login,
    logout,
  };
});
