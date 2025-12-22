# naive_system/agents/drafter.py

"""
Drafter 에이전트:
Planner가 만든 개요(Plan)를 바탕으로,
실제 문장으로 구성된 상세 초안(Draft)을 작성하는 역할.
"""

from naive_system.prompts import DRAFTER_SYSTEM_PROMPT
from naive_system.utils.llm_client import call_gemini


def build_drafter_prompt(plan: str) -> str:
    """
    Drafter에게 전달할 프롬프트를 구성한다.
    - 시스템 역할 설명(DRAFTER_SYSTEM_PROMPT)
    - Planner의 개요(plan)
    """
    full_prompt = f"""{DRAFTER_SYSTEM_PROMPT}

[Planner의 개요]
{plan}
"""
    return full_prompt


def run_drafter(plan: str) -> str:
    """
    Drafter 단계 전체 수행:
    1) Planner의 개요를 바탕으로 프롬프트 구성
    2) Gemini 호출
    3) 작성된 초안(Draft) 텍스트 반환
    """
    prompt = build_drafter_prompt(plan)
    result = call_gemini(prompt)
    return result.strip()