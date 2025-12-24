from dotenv import load_dotenv
import os 

# ⭐ 실행 시점에 딱 한 번 .env 로드
load_dotenv()



from naive_system.pipeline import run_naive_pipeline

def main():
    # 파이프라인 실행
    result = run_naive_pipeline()

    print("===== [QUESTION] =====")
    print(result.question.strip())

    print("\n===== [1. PLANNER OUTPUT] =====")
    print(result.plan.strip())

    # [NEW] Drafter가 작성한 초안 확인
    print("\n===== [2. DRAFTER OUTPUT] =====")
    print(result.draft.strip())

    # [UPDATE] Critic의 비평 (초안에 대한 피드백)
    print("\n===== [3. CRITIC OUTPUT] =====")
    print(result.critique.strip())

    # [UPDATE] Summarizer -> Editor로 명칭 변경!
    print("\n===== [4. FINAL ANSWER (EDITOR)] =====")
    print(result.final_answer.strip())


if __name__ == "__main__":
    main()