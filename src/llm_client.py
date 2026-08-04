"""
LLM Client dùng chung — tự detect API key có sẵn trong .env và trỏ đúng provider.

Thứ tự ưu tiên (khớp với comment trong .env.example):
    1. OPENROUTER_API_KEY — khuyến nghị chính, nhiều model :free
    2. OPENAI_API_KEY      — fallback nếu OpenRouter rate-limit (429)
    3. GEMINI_API_KEY      — fallback cuối, dùng endpoint OpenAI-compatible của Google

Mỗi thành viên trong nhóm chỉ cần điền key mình có vào .env local (không commit) —
code tự chọn đúng provider, không ai phải sửa code của người khác.

Cả 3 provider đều expose interface OpenAI-compatible nên dùng chung 1 client
(package `openai`), chỉ khác base_url + model id mặc định.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# (base_url, default_model) cho từng provider
_PROVIDERS = {
    "openrouter": ("https://openrouter.ai/api/v1", "openai/gpt-4o-mini"),
    "openai": (None, "gpt-4o-mini"),  # None -> dùng default base_url của SDK
    "gemini": ("https://generativelanguage.googleapis.com/v1beta/openai/", "gemini-flash-latest"),
}


def get_llm_client(model: str | None = None) -> tuple[OpenAI, str]:
    """
    Trả về (client, model_id) dựa trên API key đầu tiên tìm thấy trong .env.

    Args:
        model: model id muốn override; nếu None dùng default model của provider được chọn.

    Raises:
        RuntimeError: nếu không có key nào trong .env.
    """
    if os.getenv("OPENROUTER_API_KEY"):
        base_url, default_model = _PROVIDERS["openrouter"]
        api_key = os.getenv("OPENROUTER_API_KEY")
    elif os.getenv("OPENAI_API_KEY"):
        base_url, default_model = _PROVIDERS["openai"]
        api_key = os.getenv("OPENAI_API_KEY")
    elif os.getenv("GEMINI_API_KEY"):
        base_url, default_model = _PROVIDERS["gemini"]
        api_key = os.getenv("GEMINI_API_KEY")
    else:
        raise RuntimeError(
            "Không tìm thấy API key nào trong .env "
            "(OPENROUTER_API_KEY / OPENAI_API_KEY / GEMINI_API_KEY)"
        )

    client = OpenAI(api_key=api_key, base_url=base_url)
    return client, (model or default_model)


if __name__ == "__main__":
    client, model = get_llm_client()
    print(f"Provider detected -> model mặc định: {model}, base_url: {client.base_url}")
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": "Trả lời ngắn gọn: 1+1 bằng mấy?"}],
    )
    print(response.choices[0].message.content)
