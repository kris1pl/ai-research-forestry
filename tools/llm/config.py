from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _load_env_file() -> None:
    """Load repo-root `.env` into os.environ (only unset keys)."""
    root = Path(__file__).resolve().parents[2]
    env_file = root / ".env"
    if not env_file.is_file():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            os.environ.setdefault(key, value)


@dataclass(frozen=True)
class LLMConfig:
    provider: str
    model: str
    vertex_project: str | None = None
    vertex_location: str | None = None
    openai_api_key: str | None = None

    @classmethod
    def from_env(cls) -> LLMConfig:
        _load_env_file()
        provider = os.environ.get("LLM_PROVIDER", "vertex").strip().lower()
        model = os.environ.get("LLM_MODEL", "").strip()

        if provider not in {"vertex", "openai"}:
            raise ValueError(
                f"Unknown LLM_PROVIDER={provider!r}. Use 'vertex' or 'openai'."
            )

        if provider == "vertex":
            if not model:
                model = "gemini-3.5-flash"
            project = os.environ.get("VERTEX_PROJECT", "").strip()
            location = os.environ.get("VERTEX_LOCATION", "global").strip()
            if not project:
                raise ValueError(
                    "VERTEX_PROJECT is required when LLM_PROVIDER=vertex "
                    "(e.g. conifer-vision01)."
                )
            return cls(
                provider=provider,
                model=model,
                vertex_project=project,
                vertex_location=location,
            )

        if not model:
            model = "gpt-4o-mini"
        api_key = os.environ.get("OPENAI_API_KEY", "").strip()
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY is required when LLM_PROVIDER=openai."
            )
        return cls(
            provider=provider,
            model=model,
            openai_api_key=api_key,
        )
