# naive_system/agents/editor.py

"""
Editor 에이전트:
초안(Draft)과 Critic의 피드백(Critique)을 종합하여
최종 완성본(Final Answer)을 작성하는 역할.
"""

from naive_system.prompts import EDITOR_SYSTEM_PROMPT
from naive_system.utils.llm_client import call_gemini


def build_editor_prompt(draft: str, critique: str) -> str:
    """
    Editor에게 전달할 프롬프트를 구성한다.
    - 시스템 역할 설명
    - 원본 초안(draft)
    - Critic의 지적사항(critique)
    """
    full_prompt = f"""{EDITOR_SYSTEM_PROMPT}

[현재 초안]
{draft}

[Critic의 피드백]
{critique}
"""
    return full_prompt


def run_editor(draft: str, critique: str) -> str:
    """
    Editor 단계 전체 수행:
    1) 초안 + 피드백으로 프롬프트 구성
    2) Gemini 호출
    3) 최종 수정된 답변 반환
    """
    prompt = build_editor_prompt(draft, critique)
    result = call_gemini(prompt)
    return result.strip()