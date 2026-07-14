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

export interface KnowledgeBaseDocumentsResponse {
  items: KnowledgeBaseDocumentItem[];
  total: number;
}

export const getKnowledgeBaseDocuments = async (id: string | number, status?: string) => {
  const params: Record<string, string> = {};
  if (status) params.status = status;
  const response = await http.get<ApiResponse<KnowledgeBaseDocumentsResponse>>(
    `/api/knowledge-bases/${id}/documents`,
    { params }
  );
  return response.data;
};

export interface SearchDocumentItem {
  id: number;
  filename: string;
  status: string;
  snippet: string;
  updated_at: string;
}

export const searchKnowledgeBaseDocuments = async (
  id: string | number,
  params: { q: string; status?: string; page?: number; pageSize?: number }
) => {
  const response = await http.get<
    ApiResponse<PaginatedData<SearchDocumentItem>>
  >(`/api/knowledge-bases/${id}/search`, { params });
  return response.data;
};

export interface DocumentContentItem {
  id: number;
  name: string;
  status: string;
  content: string;
  created_at: string;
}

export const processDocument = async (id: number) => {
  const response = await http.post<ApiResponse<any>>(`/api/documents/${id}/process`);
  return response.data;
};

export const getDocumentContent = async (kbId: string | number, docId: number) => {
  const response = await http.get<ApiResponse<DocumentContentItem>>(
    `/api/knowledge-bases/${kbId}/documents/${docId}/content`
  );
  return response.data;
};

export interface ChatStreamCallbacks {
  onToken: (token: string) => void;
  onSources: (sources: any[]) => void;
  onDone: () => void;
  onError: (error: Error) => void;
}

export interface ChatSessionMessage {
  id?: number;
  role: "user" | "assistant";
  content: string;
  created_at?: string;
}

export interface ChatSessionItem {
  id: number;
  knowledge_base_id: number;
  title: string;
  created_at: string;
  updated_at: string;
  messages: ChatSessionMessage[];
}

export interface ChatSessionsResponseData {
  items: ChatSessionItem[];
  active_session: ChatSessionItem | null;
}

export const getChatSessions = async (kbId: string | number) => {
  const response = await http.get<ApiResponse<ChatSessionsResponseData>>(
    `/api/knowledge-bases/${kbId}/chat/sessions`
  );
  return response.data;
};

export const saveChatSession = async (
  kbId: string | number,
  payload: { session_id?: number | null; messages: ChatSessionMessage[] }
) => {
  const response = await http.post<ApiResponse<ChatSessionItem>>(
    `/api/knowledge-bases/${kbId}/chat/sessions`,
    payload
  );
  return response.data;
};

export const chatStream = (
  kbId: number,
  payload: { query: string; history?: { role: string; content: string }[]; top_k?: number },
  callbacks: ChatStreamCallbacks
): AbortController => {
  const controller = new AbortController();
  const token = localStorage.getItem("ai-kb-token");

  (async () => {
    try {
      const response = await fetch(
        `http://127.0.0.1:8000/api/knowledge-bases/${kbId}/chat/stream`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            ...(token ? { Authorization: `Bearer ${token}` } : {}),
          },
          body: JSON.stringify(payload),
          signal: controller.signal,
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error("Response body is not readable");
      }

      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop() || "";

        for (const line of lines) {
          if (!line.startsWith("data: ")) continue;
          try {
            const event = JSON.parse(line.slice(6));
            switch (event.type) {
              case "token":
                callbacks.onToken(event.content);
                break;
              case "sources":
                callbacks.onSources(event.data);
                break;
              case "done":
                callbacks.onDone();
                break;
            }
          } catch {
            // skip malformed events
          }
        }
      }
    } catch (err: any) {
      if (err.name === "AbortError") return;
      callbacks.onError(err instanceof Error ? err : new Error(String(err)));
    }
  })();

  return controller;
};

export interface KnowledgeBaseSettingItem {
  id: number;
  knowledge_base_id: number;
  top_k: number;
  similarity_threshold: number;
  system_prompt: string | null;
  temperature: number;
  max_tokens: number;
  model_name: string | null;
  hybrid_search: boolean;
  hybrid_alpha: number;
  updated_at: string;
}

export interface ModelOption {
  id: string;
  name: string;
}

export interface UpdateKnowledgeBaseSettingPayload {
  top_k?: number;
  similarity_threshold?: number;
  system_prompt?: string | null;
  temperature?: number;
  max_tokens?: number;
  model_name?: string | null;
  hybrid_search?: boolean;
  hybrid_alpha?: number;
}

export const listModels = async () => {
  const response = await http.get<ApiResponse<ModelOption[]>>("/api/models");
  return response.data;
};

export const getKnowledgeBaseSettings = async (id: string | number) => {
  const response = await http.get<ApiResponse<KnowledgeBaseSettingItem>>(
    `/api/knowledge-bases/${id}/settings`
  );
  return response.data;
};

export const updateKnowledgeBaseSettings = async (
  id: string | number,
  payload: UpdateKnowledgeBaseSettingPayload
) => {
  const response = await http.put<ApiResponse<KnowledgeBaseSettingItem>>(
    `/api/knowledge-bases/${id}/settings`,
    payload
  );
  return response.data;
};

export const getUploadUrl = (knowledgeBaseId: string | number) =>
  `http://127.0.0.1:8000/api/knowledge-bases/${knowledgeBaseId}/documents`;

export const getUploadHeaders = () => {
  const token = localStorage.getItem("ai-kb-token");
  return token ? { Authorization: `Bearer ${token}` } : {};
};
