from __future__ import annotations

from google import genai
from google.genai import types

from tools.llm.config import LLMConfig
from tools.llm.types import ChatMessage, LLMResponse


def _split_messages(
    messages: list[ChatMessage],
) -> tuple[str | None, list[types.Content]]:
    system_parts: list[str] = []
    contents: list[types.Content] = []

    for message in messages:
        role = message.role.strip().lower()
        if role == "system":
            system_parts.append(message.content)
            continue
        if role == "assistant":
            contents.append(
                types.Content(
                    role="model",
                    parts=[types.Part(text=message.content)],
                )
            )
            continue
        contents.append(
            types.Content(
                role="user",
                parts=[types.Part(text=message.content)],
            )
        )

    system_instruction = "\n\n".join(system_parts) if system_parts else None
    return system_instruction, contents


def _thinking_level(model_name: str) -> str | None:
    """Lowest thinking level the model accepts.

    Gemini 3.0–3.5 accept ``minimal``. Gemini 3.6 and later reject it
    (HTTP 400 THINKING_LEVEL_MINIMAL); their lowest level is ``low``.
    """
    name = model_name.strip().lower()
    if not name.startswith("gemini-3"):
        return None
    head = name.removeprefix("gemini-").split("-", 1)[0]
    parts = head.split(".")
    try:
        minor = int(parts[1]) if len(parts) > 1 else 0
    except ValueError:
        return "low"
    return "low" if minor >= 6 else "minimal"


class VertexLLMClient:
    def __init__(self, config: LLMConfig) -> None:
        if not config.vertex_project or not config.vertex_location:
            raise ValueError("Vertex config requires vertex_project and vertex_location.")
        self._config = config
        self._client = genai.Client(
            vertexai=True,
            project=config.vertex_project,
            location=config.vertex_location,
        )

    @classmethod
    def from_env(cls) -> VertexLLMClient:
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
        system_instruction, contents = _split_messages(messages)

        config_kwargs: dict = {"temperature": temperature}
        if system_instruction:
            config_kwargs["system_instruction"] = system_instruction
        if max_tokens is not None:
            config_kwargs["max_output_tokens"] = max_tokens
        thinking_level = _thinking_level(model_name)
        if thinking_level is not None:
            config_kwargs["thinking_config"] = types.ThinkingConfig(
                thinking_level=thinking_level,
            )

        try:
            response = self._client.models.generate_content(
                model=model_name,
                contents=contents,
                config=types.GenerateContentConfig(**config_kwargs),
            )
        except Exception as exc:  # noqa: BLE001 — surface provider errors clearly
            raise RuntimeError(
                "Vertex generate_content failed. Check ADC "
                "(gcloud auth application-default login), "
                f"VERTEX_PROJECT={self._config.vertex_project}, "
                f"VERTEX_LOCATION={self._config.vertex_location}, "
                f"and roles/aiplatform.user. Original: {exc}"
            ) from exc

        usage: dict = {}
        if response.usage_metadata is not None:
            usage = {
                "prompt_token_count": response.usage_metadata.prompt_token_count,
                "candidates_token_count": response.usage_metadata.candidates_token_count,
                "total_token_count": response.usage_metadata.total_token_count,
            }

        return LLMResponse(
            text=(response.text or "").strip(),
            model=model_name,
            usage=usage,
        )
