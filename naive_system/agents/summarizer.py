# naive_system/agents/summarizer.py

"""
Summarizer 에이전트:
질문, Planner의 계획, Critic의 피드백을 종합하여
5문장 이내의 최종 답변을 생성하는 역할.
"""

from naive_system.prompts import SUMMARIZER_SYSTEM_PROMPT
from naive_system.utils.llm_client import call_gemini


def build_summarizer_prompt(question: str, plan: str, critique: str) -> str:
    """
    Summarizer에게 전달할 최종 프롬프트를 구성한다.
    - 시스템 역할 설명(SUMMARIZER_SYSTEM_PROMPT)
    - 질문(question)
    - Planner의 계획(plan)
    - Critic의 피드백(critique)
    네 요소를 합쳐 하나의 프롬프트 문자열로 만든다.
    """
    full_prompt = f"""{SUMMARIZER_SYSTEM_PROMPT}

[질문]
{question}

[Planner의 계획]
{plan}

[Critic의 피드백]
{critique}
"""
    return full_prompt


def run_summarizer(question: str, plan: str, critique: str) -> str:
    """
    Summarizer 단계 전체 수행:
    1) 질문 + 계획 + 피드백을 바탕으로 프롬프트 구성
    2) Gemini 호출
    3) 5문장 이내의 최종 답변 텍스트 반환
    """
    prompt = build_summarizer_prompt(question, plan, critique)
    result = call_gemini(prompt)
    return result.strip()