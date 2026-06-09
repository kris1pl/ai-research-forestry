from __future__ import annotations

from typing import TYPE_CHECKING

from tools.llm.config import LLMConfig

if TYPE_CHECKING:
    from tools.llm.protocol import LLMClient


def get_llm_client(config: LLMConfig | None = None) -> LLMClient:
    cfg = config or LLMConfig.from_env()
    if cfg.provider == "vertex":
        from tools.llm.vertex_client import VertexLLMClient

        return VertexLLMClient(cfg)
    if cfg.provider == "openai":
        from tools.llm.openai_client import OpenAILLMClient

        return OpenAILLMClient(cfg)
    raise ValueError(f"Unknown LLM_PROVIDER: {cfg.provider}")
