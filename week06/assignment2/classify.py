import json
import re
from mock_llm import mock_llm_call

def classify_review(review_text: str, system_prompt: str = "", use_regex_fix: bool = False) -> dict | None:
    """
    리뷰 텍스트를 LLM에 전달하고, 응답 텍스트를 방어 로직을 통해 JSON 파싱한다.
    """
    # 1. Mock LLM 호출 및 text 추출
    response = mock_llm_call(system=system_prompt, user_message=review_text)
    raw_text = response["text"].strip()

    # [방어 1] 코드펜스(```json ... ```) 제거
    if raw_text.startswith("```"):
        raw_text = re.sub(r"^```(?:json)?\n?", "", raw_text, flags=re.IGNORECASE)
        raw_text = re.sub(r"\n?```$", "", raw_text)
        raw_text = raw_text.strip()

    # [선택 도전 과제] 정규식을 사용하여 { ... } 부분만 추출 (사족형 복구용)
    if use_regex_fix:
        match = re.search(r"\{[\s\S]*\}", raw_text)
        if match:
            raw_text = match.group(0)

    # [방어 2] try-except 구문으로 안전 파싱 (실패 시 None 반환하여 파이프라인 유지)
    try:
        data = json.loads(raw_text)
        return data
    except (json.JSONDecodeError, TypeError):
        return None