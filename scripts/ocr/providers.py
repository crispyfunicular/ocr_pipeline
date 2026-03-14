"""
VLM provider clients, retry logic, and API call wrappers.

This module handles all direct communication with LLM providers
(OpenAI, Anthropic, Google Gemini) including client creation,
retry with exponential backoff, and the unified process_single_image()
entry point.
"""

import os
import sys
import time
import base64
from pathlib import Path

from openai import OpenAI

try:
    import anthropic as _anthropic_module
except ImportError:
    _anthropic_module = None

try:
    import google.genai as _genai_module
    from google.genai import types as _genai_types
except ImportError:
    _genai_module = None
    _genai_types = None

from scripts.ocr.core import (
    DEFAULT_MODEL,
    MAX_COMPLETION_TOKENS,
    SINGLE_IMAGE_PROMPT,
    VLMResult,
    detect_provider,
    encode_image,
    estimate_cost,
    parse_vlm_response,
)
from scripts.utils import format_cost, mime_type_for_image

# ── Client creation ────────────────────────────────────────────


def create_client(provider: str):
    """Create the appropriate API client for the given provider."""
    if provider == "anthropic":
        if _anthropic_module is None:
            print(
                "❌ anthropic package not installed. Run: pip install anthropic",
                file=sys.stderr,
            )
            sys.exit(1)
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            print("❌ ANTHROPIC_API_KEY not set.", file=sys.stderr)
            sys.exit(1)
        return _anthropic_module.Anthropic(api_key=api_key)
    elif provider == "google":
        if _genai_module is None:
            print(
                "❌ google-genai package not installed. Run: pip install google-genai",
                file=sys.stderr,
            )
            sys.exit(1)
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("❌ GEMINI_API_KEY not set.", file=sys.stderr)
            sys.exit(1)
        return _genai_module.Client(api_key=api_key)
    else:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("❌ OPENAI_API_KEY not set.", file=sys.stderr)
            sys.exit(1)
        return OpenAI(api_key=api_key)


# ── Retry logic ────────────────────────────────────────────────

_RETRYABLE_KEYWORDS = (
    "429",
    "rate limit",
    "rate_limit",
    "resource_exhausted",
    "502",
    "503",
    "504",
    "overloaded",
    "server error",
    "connection",
    "timeout",
    "timed out",
)


def _retry_api_call(fn, *, max_retries: int = 3, base_delay: float = 2.0):
    """Retry an API call with exponential backoff + jitter.

    Retries on rate limits (429), server errors (5xx), and connection issues.
    """
    import random as _rng

    for attempt in range(max_retries + 1):
        try:
            return fn()
        except Exception as e:
            err = str(e).lower()
            retryable = any(k in err for k in _RETRYABLE_KEYWORDS)
            if not retryable or attempt == max_retries:
                raise
            delay = base_delay * (2**attempt) + _rng.uniform(0, 1)
            print(
                f"  ⏳ Retry {attempt + 1}/{max_retries} in {delay:.1f}s — {str(e)[:80]}"
            )
            time.sleep(delay)


# ── Provider-specific API calls ────────────────────────────────


def _call_openai(
    client, model: str, workflow: str, user_text: str, b64: str, mime: str = "image/png"
) -> dict:
    """Call OpenAI chat completions API. Returns normalized response dict."""
    messages = [
        {"role": "system", "content": workflow},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": user_text},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{mime};base64,{b64}",
                        "detail": "high",
                    },
                },
            ],
        },
    ]

    def _do_call():
        # Try with temperature=0; some models reject it, so retry without
        try:
            return client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0,
                max_completion_tokens=MAX_COMPLETION_TOKENS,
            )
        except Exception as e:
            if "temperature" in str(e).lower():
                return client.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_completion_tokens=MAX_COMPLETION_TOKENS,
                )
            raise

    response = _retry_api_call(_do_call)
    usage = response.usage
    return {
        "text": response.choices[0].message.content,
        "prompt_tokens": usage.prompt_tokens if usage else 0,
        "completion_tokens": usage.completion_tokens if usage else 0,
    }


def _call_anthropic(
    client, model: str, workflow: str, user_text: str, b64: str, mime: str = "image/png"
) -> dict:
    """Call Anthropic Messages API. Returns normalized response dict."""

    def _do_call():
        return client.messages.create(
            model=model,
            system=workflow,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": mime,
                                "data": b64,
                            },
                        },
                        {"type": "text", "text": user_text},
                    ],
                }
            ],
            temperature=0,
            max_tokens=MAX_COMPLETION_TOKENS,
        )

    response = _retry_api_call(_do_call)
    usage = response.usage
    text = response.content[0].text if response.content else ""
    return {
        "text": text,
        "prompt_tokens": usage.input_tokens if usage else 0,
        "completion_tokens": usage.output_tokens if usage else 0,
    }


def _call_google(
    client, model: str, workflow: str, user_text: str, b64: str, mime: str = "image/png"
) -> dict:
    """Call Google Gemini API. Returns normalized response dict."""
    image_bytes = base64.b64decode(b64)

    config = _genai_types.GenerateContentConfig(
        system_instruction=workflow,
        temperature=0,
    )

    def _do_call():
        return client.models.generate_content(
            model=model,
            contents=[
                _genai_types.Part.from_bytes(data=image_bytes, mime_type=mime),
                user_text,
            ],
            config=config,
        )

    response = _retry_api_call(_do_call)
    usage = response.usage_metadata
    return {
        "text": response.text or "",
        "prompt_tokens": usage.prompt_token_count if usage else 0,
        "completion_tokens": usage.candidates_token_count if usage else 0,
    }


# ── Main processing function ──────────────────────────────────


def process_single_image(
    client,
    img_path: Path,
    workflow: str,
    model: str = DEFAULT_MODEL,
    debug: bool = False,
) -> VLMResult:
    """Send a single image to the VLM and parse the structured response."""
    b64 = encode_image(img_path)
    mime = mime_type_for_image(img_path)
    user_text = SINGLE_IMAGE_PROMPT.format(filename=img_path.name)
    provider = detect_provider(model)

    if debug:
        print(f"\n{'┄' * 60}")
        print(f"  🐛 DEBUG — Provider: {provider}")
        print(f"  🐛 DEBUG — System prompt ({len(workflow)} chars):")
        print(f"{'┄' * 60}")
        print(workflow[:2000])
        if len(workflow) > 2000:
            print(f"  ... ({len(workflow) - 2000} more chars)")
        print(f"{'┄' * 60}")
        print(f"  🐛 DEBUG — User prompt:")
        print(f"{'┄' * 60}")
        print(user_text)
        print(f"  🐛 DEBUG — Image: {img_path} ({mime}, base64 {len(b64)} chars)")
        print(f"{'┄' * 60}")

    t0 = time.time()

    if provider == "anthropic":
        result = _call_anthropic(client, model, workflow, user_text, b64, mime=mime)
    elif provider == "google":
        result = _call_google(client, model, workflow, user_text, b64, mime=mime)
    else:
        result = _call_openai(client, model, workflow, user_text, b64, mime=mime)

    elapsed = time.time() - t0
    text = result["text"]
    prompt_tokens = result["prompt_tokens"]
    completion_tokens = result["completion_tokens"]

    cost = estimate_cost(model, prompt_tokens, completion_tokens)

    if debug:
        print(f"\n{'┄' * 60}")
        print(
            f"  🐛 DEBUG — Response ({elapsed:.1f}s, {prompt_tokens}+{completion_tokens} tokens, {format_cost(cost)} est.):"
        )
        print(f"{'┄' * 60}")
        print(text)
        print(f"{'┄' * 60}")

    parsed = parse_vlm_response(text)

    return {
        **parsed,
        "raw": text,
        "elapsed": round(elapsed, 1),
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "cost": cost,
    }
