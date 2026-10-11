# week06/assignment2/mock_llm.py
import random

def mock_llm_call(system, user_message, temperature=0.2, max_tokens=500):
    """
    실제 API와 동일한 인터페이스를 갖는 모의 함수.
    20% 확률로 3가지 유형의 불량 응답 문자열을 text 키에 담아 반환한다.
    """
    reviews_keywords = {
        "배송": '{"category": "배송", "sentiment": "부정", "urgency": 3}',
        "환불": '{"category": "환불", "sentiment": "부정", "urgency": 3}',
        "품질": '{"category": "품질", "sentiment": "긍정", "urgency": 1}',
    }
    
    # 키워드 매칭 (기본값: 기타)
    canned_text = '{"category": "기타", "sentiment": "중립", "urgency": 1}'
    for keyword, canned in reviews_keywords.items():
        if keyword in user_message:
            canned_text = canned
            break

    # 20% 확률로 불량 응답 변형 생성
    if random.random() < 0.20:
        malformed_type = random.choice(["codefence", "chatter", "truncated"])
        
        if malformed_type == "codefence":
            # 유형 1: 코드펜스 포함
            canned_text = f"```json\n{canned_text}\n```"
            
        elif malformed_type == "chatter":
            # 유형 2: 사족 포함
            canned_text = f"네, 요청하신 분석 결과입니다!\n{canned_text}\n감사합니다."
            
        elif malformed_type == "truncated":
            # 유형 3: 잘린 JSON
            canned_text = '{"category": "배송", "urgency": 3, "sentim'

    # 실제 API 포맷과 동일한 딕셔너리 반환
    return {
        "text": canned_text,
        "stop_reason": "end_turn",
        "usage": {"input_tokens": 120, "output_tokens": 35}
    }