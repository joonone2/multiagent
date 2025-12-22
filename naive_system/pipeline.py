# naive_system/pipeline.py

"""
Naive 멀티에이전트 파이프라인 (Improved):
Question -> Planner -> Drafter -> Critic -> Editor
"""

from dataclasses import dataclass

from naive_system.prompts import MAIN_QUESTION
from naive_system.agents.planner import run_planner
from naive_system.agents.drafter import run_drafter
from naive_system.agents.critic import run_critic
from naive_system.agents.editor import run_editor


@dataclass
class NaiveResult:
    """파이프라인의 각 단계 결과를 모두 저장하는 데이터 구조."""
    question: str
    plan: str
    draft: str
    critique: str
    final_answer: str


def run_naive_pipeline(question: str | None = None) -> NaiveResult:
    """
    개선된 Naive 멀티에이전트 파이프라인 실행:
    1) Planner: 질문을 보고 개요(Plan) 생성
    2) Drafter: 개요를 바탕으로 상세 초안(Draft) 작성
    3) Critic: 초안을 읽고 비평(Critique) 및 개선점 지적
    4) Editor: 초안과 비평을 종합해 최종 답변(Final Answer) 완성
    """
    if question is None:
        question = MAIN_QUESTION

    # 1단계: Planner (기획)
    plan = run_planner(question)

    # 2단계: Drafter (집필)
    draft = run_drafter(plan)

    # 3단계: Critic (교정)
    critique = run_critic(draft)

    # 4단계: Editor (편집)
    final_answer = run_editor(draft, critique)

    return NaiveResult(
        question=question,
        plan=plan,
        draft=draft,
        critique=critique,
        final_answer=final_answer,
    )