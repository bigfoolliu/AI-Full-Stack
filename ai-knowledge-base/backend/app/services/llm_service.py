import json
from typing import Generator

from openai import OpenAI

from app.core.config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL, MAX_HISTORY_TOKENS


class LlmService:
    """封装 LLM 定时/流式对话及消息组装。"""

    def __init__(self):
        self.model = LLM_MODEL
        self.client = (
            OpenAI(
                api_key=LLM_API_KEY,
                base_url=LLM_BASE_URL,
            )
            if LLM_API_KEY
            else None
        )

    def chat(
        self,
        query: str,
        context_chunks: list[dict],
        history: list[dict] | None = None,
        system_prompt: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        model: str | None = None,
    ) -> dict:
        """非流式 LLM 对话，返回 answer + sources。"""
        if not self.client:
            return {
                "answer": "LLM API Key 未配置，无法回答问题。请设置 LLM_API_KEY 或 DASHSCOPE_API_KEY。",
                "sources": context_chunks,
            }

        messages = self._build_messages(query, context_chunks, history, system_prompt)

        response = self.client.chat.completions.create(
            model=model or self.model,
            messages=messages,
            temperature=temperature if temperature is not None else 0.7,
            max_tokens=max_tokens if max_tokens is not None else 2048,
        )

        answer = response.choices[0].message.content or ""

        return {
            "answer": answer,
            "sources": context_chunks,
        }

    def chat_stream(
        self,
        query: str,
        context_chunks: list[dict],
        history: list[dict] | None = None,
        system_prompt: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        model: str | None = None,
        metrics: dict | None = None,
    ) -> Generator[str, None, None]:
        """流式生成 SSE 事件：token → sources → metrics → done。"""
        if not self.client:
            yield f"data: {json.dumps({'type': 'token', 'content': 'LLM API Key 未配置，无法回答问题。'})}\n\n"
            yield f"data: {json.dumps({'type': 'sources', 'data': context_chunks})}\n\n"
            if metrics:
                yield f"data: {json.dumps({'type': 'metrics', 'data': metrics})}\n\n"
            yield f"data: {json.dumps({'type': 'done'})}\n\n"
            return

        messages = self._build_messages(query, context_chunks, history, system_prompt)

        stream = self.client.chat.completions.create(
            model=model or self.model,
            messages=messages,
            temperature=temperature if temperature is not None else 0.7,
            max_tokens=max_tokens if max_tokens is not None else 2048,
            stream=True,
        )

        for chunk in stream:
            delta = chunk.choices[0].delta if chunk.choices else None
            if delta and delta.content:
                yield f"data: {json.dumps({'type': 'token', 'content': delta.content})}\n\n"

        yield f"data: {json.dumps({'type': 'sources', 'data': context_chunks})}\n\n"
        if metrics:
            yield f"data: {json.dumps({'type': 'metrics', 'data': metrics})}\n\n"
        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    DEFAULT_SYSTEM_PROMPT = (
        "你是一个知识库问答助手。\n"
        "请基于以下检索到的文档内容回答用户的问题。\n"
        "如果文档内容不足以回答，请如实告知，不要编造。"
    )

    def _build_messages(
        self,
        query: str,
        context_chunks: list[dict],
        history: list[dict] | None = None,
        custom_system_prompt: str | None = None,
    ) -> list[dict]:
        """构建 system + history + user 消息列表，按 token 预算裁剪历史。"""
        system_prompt = self._build_system_prompt(context_chunks, custom_system_prompt)
        messages: list[dict] = []
        chars_budget = MAX_HISTORY_TOKENS * 4

        if history:
            trimmed: list[dict] = []
            chars_used = len(system_prompt) + len(query)
            for msg in reversed(history):
                if msg.get("role") not in ("user", "assistant"):
                    continue
                msg_chars = len(msg.get("content", ""))
                if chars_used + msg_chars > chars_budget:
                    break
                trimmed.insert(0, msg)
                chars_used += msg_chars
            messages.extend(trimmed)

        messages.insert(0, {"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": query})
        return messages

    @staticmethod
    def _build_system_prompt(context_chunks: list[dict], custom_prompt: str | None = None) -> str:
        """将检索上下文追加到系统 prompt 尾部。"""
        base_prompt = (custom_prompt or LlmService.DEFAULT_SYSTEM_PROMPT).strip()

        if not context_chunks:
            if custom_prompt:
                return base_prompt + "\n\n当前知识库中没有检索到与问题相关的内容，请如实告知用户，不要编造信息。"
            return base_prompt

        context_lines = []
        for i, chunk in enumerate(context_chunks, 1):
            source = chunk.get("filename", "未知文档")
            content = chunk.get("content", "")
            context_lines.append(f"[{i}] 来源：{source}\n{content}")

        context_str = "\n\n".join(context_lines)

        return f"{base_prompt}\n\n检索到的相关内容：\n{context_str}\n"
