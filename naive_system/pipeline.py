# naive_system/pipeline.py

"""
Naive 멀티에이전트 파이프라인:
question -> planner -> critic -> summarizer
전체 워크플로우를 하나의 함수로 묶어준다.
"""

from dataclasses import dataclass

from naive_system.prompts import MAIN_QUESTION
from naive_system.agents.planner import run_planner
from naive_system.agents.critic import run_critic
from naive_system.agents.summarizer import run_summarizer


@dataclass
class NaiveResult:
    """Naive 파이프라인의 전체 결과를 담는 데이터 구조."""
    question: str
    plan: str
    critique: str
    final_answer: str


def run_naive_pipeline(question: str | None = None) -> NaiveResult:
    """
    Naive 멀티에이전트 파이프라인을 실행한다.

    1) Planner: 질문을 보고 답변 아웃라인(계획)을 생성
    2) Critic: 계획의 약점과 개선점을 지적
    3) Summarizer: 질문 + 계획 + 피드백을 종합해 5문장 이내 최종 답변 생성
    """
    if question is None:
        question = MAIN_QUESTION

    # 1단계: Planner
    plan = run_planner(question)

    # 2단계: Critic
    critique = run_critic(plan)

    # 3단계: Summarizer
    final_answer = run_summarizer(question, plan, critique)

    return NaiveResult(
        question=question,
        plan=plan,
        critique=critique,
        final_answer=final_answer,
    )