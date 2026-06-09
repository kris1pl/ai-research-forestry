#!/usr/bin/env python3
"""Smoke test for tools.llm — one completion via configured provider."""

from __future__ import annotations

import sys

from tools.llm import ChatMessage, get_llm_client


def main() -> None:
    try:
        client = get_llm_client()
        response = client.complete(
            [ChatMessage("user", "Reply with exactly: OK")],
            temperature=0.0,
        )
    except (ValueError, RuntimeError) as exc:
        raise SystemExit(f"LLM smoke test failed: {exc}") from exc

    preview = response.text[:200]
    model = response.model or "(unknown)"
    print(f"model: {model}")
    print(f"response: {preview!r}")
    if response.usage:
        print(f"usage: {response.usage}")


if __name__ == "__main__":
    main()
