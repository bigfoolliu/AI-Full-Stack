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
  pageSize = 10
) => {
  const response = await http.get<ApiResponse<PaginatedData<KnowledgeBaseItem>>>(
    "/api/knowledge-bases",
    { params: { page, page_size: pageSize } }
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

export const getKnowledgeBaseDocuments = async (id: string | number) => {
  const response = await http.get<ApiResponse<KnowledgeBaseDocumentItem[]>>(
    `/api/knowledge-bases/${id}/documents`
  );
  return response.data;
};

export const getUploadUrl = (knowledgeBaseId: string | number) =>
  `http://127.0.0.1:8000/api/knowledge-bases/${knowledgeBaseId}/documents`;

export const getUploadHeaders = () => {
  const token = localStorage.getItem("ai-kb-token");
  return token ? { Authorization: `Bearer ${token}` } : {};
};
