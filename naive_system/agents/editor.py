from naive_system.prompts import EDITOR_SYSTEM_PROMPT
from naive_system.utils.llm_client import call_gemini

"""
Editor 에이전트:
Drafter의 초안(Draft)과 Critic의 비평(Critique)을 반영하여
사용자 질문에 대한 최종 답변(Final Answer)을 작성
"""

def build_editor_prompt(question: str, draft: str, critique: str) -> str:
    """
    Editor에게 전달할 프롬프트를 구성
    - 시스템 역할 설명(EDITOR_SYSTEM_PROMPT)
    - 원래 질문(question), 초안(draft), 비평(critique)
    위 요소들을 조합하여 수정 지침을 포함한 프롬프트 생성
    """
    full_prompt = f"""{EDITOR_SYSTEM_PROMPT}

        [원래 질문]
        {question}

        [현재 초안]
        {draft}

        [Critic의 피드백]
        {critique}
        """
    return full_prompt

def run_editor(question: str, draft: str, critique: str) -> str:
    """
    Editor 에이전트 실행
    - 프롬프트 구성 후 Gemini 호출
    - 최종 수정된 답변 반환
    """
    prompt = build_editor_prompt(question, draft, critique)
    result = call_gemini(prompt)
    return result.strip()