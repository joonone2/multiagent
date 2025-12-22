print("🔥 test_gemini 시작")

# 🔥 중요! .env 반드시 로드
from dotenv import load_dotenv
load_dotenv()

from naive_system.utils.llm_client import call_gemini
print("✅ llm_client import 완료")

def main():
    print("💬 main() 진입")
    prompt = "한 문장으로 너가 누구인지 한국어로 소개해줘."
    print("💬 call_gemini 호출 직전")
    text = call_gemini(prompt)
    print("💬 call_gemini 반환 완료")
    print("=== Gemini 응답 ===")
    print(text)

if __name__ == "__main__":
    print("⚙️ __main__ 진입")
    main()