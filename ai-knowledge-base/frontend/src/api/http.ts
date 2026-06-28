import axios from "axios";

const STORAGE_TOKEN_KEY = "ai-kb-token";

export const http = axios.create({
  baseURL: "http://127.0.0.1:8000",
  timeout: 10000,
});

// 请求拦截器：每次发HTTP请求之前统一执行
http.interceptors.request.use((config) => {
  const token = localStorage.getItem(STORAGE_TOKEN_KEY);

  if (token) {
    // Bearer 是JWT标准鉴权前缀，后端固定解析格式
    config.headers.Authorization = `Bearer ${token}`;
  }

  // 返回处理后的请求配置，放行本次请求
  return config;
});
