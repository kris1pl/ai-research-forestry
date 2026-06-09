from __future__ import annotations

from openai import OpenAI

from tools.llm.config import LLMConfig
from tools.llm.types import ChatMessage, LLMResponse


class OpenAILLMClient:
    def __init__(self, config: LLMConfig) -> None:
        if not config.openai_api_key:
            raise ValueError("OpenAI config requires openai_api_key.")
        self._config = config
        self._client = OpenAI(api_key=config.openai_api_key)

    @classmethod
    def from_env(cls) -> OpenAILLMClient:
        return cls(LLMConfig.from_env())

    def complete(
        self,
        messages: list[ChatMessage],
        *,
        model: str | None = None,
        temperature: float = 0.2,
        max_tokens: int | None = None,
    ) -> LLMResponse:
        if not messages:
            raise ValueError("messages must not be empty")

        model_name = model or self._config.model
        payload = [
            {"role": message.role, "content": message.content} for message in messages
        ]

        kwargs: dict = {
            "model": model_name,
            "messages": payload,
            "temperature": temperature,
        }
        if max_tokens is not None:
            kwargs["max_tokens"] = max_tokens

        try:
            response = self._client.chat.completions.create(**kwargs)
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError(
                "OpenAI chat.completions.create failed. "
                "Check OPENAI_API_KEY and LLM_MODEL. "
                f"Original: {exc}"
            ) from exc

        choice = response.choices[0]
        usage: dict = {}
        if response.usage is not None:
            usage = {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            }

        return LLMResponse(
            text=(choice.message.content or "").strip(),
            model=response.model or model_name,
            usage=usage,
        )
