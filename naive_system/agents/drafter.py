from naive_system.prompts import DRAFTER_SYSTEM_PROMPT
from naive_system.utils.llm_client import call_gemini


"""
Drafter 에이전트:
Planner가 만든 개요(Plan)를 바탕으로,
실제 문장으로 구성된 상세 초안(Draft)을 작성하는 역할.
"""

def build_drafter_prompt(question: str, plan: str) -> str:
    """
    Drafter에게 전달할 프롬프트를 구성
    - 시스템 역할 설명(DRAFTER_SYSTEM_PROMPT)
    - Planner의 개요(plan)
    """
    full_prompt = f"""{DRAFTER_SYSTEM_PROMPT}

        [사용자 질문]
        {question}

        [Planner의 개요]
        {plan}
        """
    return full_prompt

def run_drafter(question: str, plan: str) -> str:
    # 인자 추가됨: question
    prompt = build_drafter_prompt(question, plan)
    result = call_gemini(prompt)
    return result.strip()