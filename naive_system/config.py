# naive_system/config.py 혹은 utils/config.py 이런 느낌일 거라 가정

import os

def get_gemini_api_key() -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY가 환경변수에 설정되어 있지 않습니다. "
            ".env 로드 위치 또는 키 이름을 확인해주세요."
        )
    return api_key


def get_default_model_name() -> str:
    """나이브 시스템에서 기본으로 사용할 Gemini 모델 이름."""
    return "gemini-2.5-flash"