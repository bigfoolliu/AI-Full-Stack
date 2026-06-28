import { http } from "./http";

// 后端统一返回的通用接口结构体
interface ApiResponse<T> {
  code: number;
  message: string;
  data: T;
}

// 登录接口请求入参
export interface LoginPayload {
  username: string;
  password: string;
}

// 用户基础信息结构
export interface UserInfo {
  id: number;
  username: string;
  nickname: string;
}

// 登录成功后接口返回的data内部结构
export interface LoginResponseData {
  token: string;
  user: UserInfo;
}

// 登录接口请求函数
export const login = async (payload: LoginPayload) => {
  const response = await http.post<ApiResponse<LoginResponseData>>(
    "/api/login",
    payload
  );
  return response.data;
};

// 获取当前登录用户信息接口
export const getMe = async () => {
  const response = await http.get<ApiResponse<UserInfo>>("/api/me");
  return response.data;
};
