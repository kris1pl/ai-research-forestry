from __future__ import annotations

from typing import Protocol

from tools.llm.types import ChatMessage, LLMResponse


class LLMClient(Protocol):
    def complete(
        self,
        messages: list[ChatMessage],
        *,
        model: str | None = None,
        temperature: float = 0.2,
        max_tokens: int | None = None,
    ) -> LLMResponse: ...
