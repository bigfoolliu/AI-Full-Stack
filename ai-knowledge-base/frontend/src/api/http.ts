import axios from "axios";
import { ElMessage } from "element-plus";

let redirecting = false;

export const http = axios.create({
  baseURL: "http://127.0.0.1:8000",
  timeout: 10000,
});

http.interceptors.request.use((config) => {
  const token = localStorage.getItem("ai-kb-token");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

http.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401 && !redirecting) {
      const isLoginRequest = error.config?.url === "/api/login";
      if (!isLoginRequest) {
        redirecting = true;
        localStorage.removeItem("ai-kb-token");
        localStorage.removeItem("ai-kb-username");
        localStorage.removeItem("ai-kb-nickname");
        ElMessage.error("登录已过期，请重新登录");
        setTimeout(() => {
          window.location.href = "/login";
        }, 500);
      }
    }
    return Promise.reject(error);
  }
);
