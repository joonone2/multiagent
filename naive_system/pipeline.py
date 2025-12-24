# naive_system/pipeline.py

from dataclasses import dataclass
from naive_system.prompts import MAIN_QUESTION
from naive_system.agents.planner import run_planner
from naive_system.agents.drafter import run_drafter
from naive_system.agents.critic import run_critic
from naive_system.agents.editor import run_editor

@dataclass
class NaiveResult:
    question: str
    plan: str
    draft: str
    critique: str
    final_answer: str

def run_naive_pipeline(question: str | None = None) -> NaiveResult:
    if question is None:
        question = MAIN_QUESTION

    # 1. Planner (질문 -> 계획)
    print("1. Planner 실행...", flush=True)
    plan = run_planner(question)
    print(f"\n[Planner 결과]\n{plan}\n" + "-"*30 + "\n", flush=True)

    # 2. Drafter (질문 + 계획 -> 초안)  <-- 수정됨
    print("2. Drafter 실행...", flush=True)
    draft = run_drafter(question, plan)
    print(f"\n[Drafter 결과]\n{draft}\n" + "-"*30 + "\n", flush=True)

    # 3. Critic (질문 + 계획 + 초안 -> 비평) <-- 수정됨
    print("3. Critic 실행...", flush=True)
    critique = run_critic(question, plan, draft)
    print(f"\n[Critic 결과]\n{critique}\n" + "-"*30 + "\n", flush=True)

    # 4. Editor (질문 + 초안 + 비평 -> 최종답) <-- 수정됨
    print("4. Editor 실행...", flush=True)
    final_answer = run_editor(question, draft, critique)
    print(f"\n[Editor 결과]\n{final_answer}\n" + "-"*30 + "\n", flush=True)

    print("완료.", flush=True)

    return NaiveResult(question, plan, draft, critique, final_answer)