from dotenv import load_dotenv
import os 
# ⭐ 실행 시점에 딱 한 번 .env 로드
load_dotenv()
print("[DEBUG] GEMINI_API_KEY right after load_dotenv in run_naive.py:", repr(os.getenv("GEMINI_API_KEY")))


from naive_system.pipeline import run_naive_pipeline


def main():
    result = run_naive_pipeline()

    print("===== [QUESTION] =====")
    print(result.question.strip())

    print("\n===== [PLANNER OUTPUT] =====")
    print(result.plan.strip())

    print("\n===== [CRITIC OUTPUT] =====")
    print(result.critique.strip())

    print("\n===== [FINAL ANSWER (SUMMARIZER)] =====")
    print(result.final_answer.strip())


if __name__ == "__main__":
    main()