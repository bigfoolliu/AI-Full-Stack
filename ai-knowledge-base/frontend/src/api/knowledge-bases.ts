import { http } from "./http";

interface ApiResponse<T> {
  code: number;
  message: string;
  data: T;
}

export interface CreateKnowledgeBasePayload {
  name: string;
  description: string;
}

export interface KnowledgeBaseItem {
  id: number;
  name: string;
  description: string;
  document_count: number;
  created_at: string;
}

export interface PaginatedData<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
}

export interface KnowledgeBaseDocumentItem {
  id: number;
  name: string;
  status: string;
  updated_at: string;
}

export const getKnowledgeBases = async (
  page = 1,
  pageSize = 10,
  keyword?: string
) => {
  const params: Record<string, number | string> = { page, page_size: pageSize };
  if (keyword) params.keyword = keyword;
  const response = await http.get<ApiResponse<PaginatedData<KnowledgeBaseItem>>>(
    "/api/knowledge-bases",
    { params }
  );
  return response.data;
};

export const createKnowledgeBase = async (
  payload: CreateKnowledgeBasePayload
) => {
  const response = await http.post<ApiResponse<KnowledgeBaseItem>>(
    "/api/knowledge-bases",
    payload
  );
  return response.data;
};

export const getKnowledgeBaseDetail = async (id: string | number) => {
  const response = await http.get<ApiResponse<KnowledgeBaseItem>>(
    `/api/knowledge-bases/${id}`
  );
  return response.data;
};

export const getKnowledgeBaseDocuments = async (id: string | number, status?: string) => {
  const params: Record<string, string> = {};
  if (status) params.status = status;
  const response = await http.get<ApiResponse<KnowledgeBaseDocumentItem[]>>(
    `/api/knowledge-bases/${id}/documents`,
    { params }
  );
  return response.data;
};

export const getUploadUrl = (knowledgeBaseId: string | number) =>
  `http://127.0.0.1:8000/api/knowledge-bases/${knowledgeBaseId}/documents`;

export const getUploadHeaders = () => {
  const token = localStorage.getItem("ai-kb-token");
  return token ? { Authorization: `Bearer ${token}` } : {};
};
