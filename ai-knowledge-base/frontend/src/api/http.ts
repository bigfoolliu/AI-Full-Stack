import axios from "axios";
import { ElMessage } from "element-plus";

let redirecting = false;

export const http = axios.create({
  baseURL: import.meta.env.DEV ? "http://127.0.0.1:8000" : "",
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
    const status = error.response?.status;
    if (status === 401 && !redirecting) {
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
    } else if (status === 403) {
      ElMessage.error("没有权限执行此操作");
    } else if (status === 404) {
      ElMessage.error("请求的资源不存在");
    } else if (status && status >= 500) {
      ElMessage.error("服务器错误，请稍后重试");
    } else if (!error.response) {
      ElMessage.error("网络错误，请检查网络连接");
    }
    return Promise.reject(error);
  }
);
