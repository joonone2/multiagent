import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

import os
from google import genai
from naive_system.config import get_gemini_api_key, get_default_model_name

def call_gemini(prompt: str) -> str:
    api_key = get_gemini_api_key()
    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model=get_default_model_name(),
            contents=prompt,
        )

        # 응답 텍스트 추출 
        return response.text

    except Exception as e:
        print("❌ [ERROR] call_gemini 예외 발생:", e)
        raise e