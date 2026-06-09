from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ChatMessage:
    role: str
    content: str


@dataclass
class LLMResponse:
    text: str
    model: str | None = None
    usage: dict[str, Any] = field(default_factory=dict)
