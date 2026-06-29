import { http } from "./http";

interface ApiResponse<T> {
  code: number;
  message: string;
  data: T;
}

export interface KnowledgeBaseItem {
  id: number;
  name: string;
  description: string;
  document_count: number;
  created_at: string;
}

export const getKnowledgeBases = async () => {
  const response = await http.get<ApiResponse<KnowledgeBaseItem[]>>(
    "/api/knowledge-bases"
  );
  return response.data;
};
