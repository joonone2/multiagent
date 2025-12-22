"""
Critic 에이전트:
Planner가 만든 아웃라인(계획)을 읽고,
논리적 약점, 누락된 관점, 모호한 부분을 지적하고
개선 방향을 제안하는 역할.
"""

from naive_system.prompts import CRITIC_SYSTEM_PROMPT
from naive_system.utils.llm_client import call_gemini

def build_critic_prompt(draft: str) -> str:
    """
    Critic에게 전달할 프롬프트를 구성한다.
    - 시스템 역할 설명(CRITIC_SYSTEM_PROMPT)
    - Drafter가 쓴 초안(draft)
    """
    full_prompt = f"""{CRITIC_SYSTEM_PROMPT}

[작성된 초안]
{draft}
"""
    return full_prompt


def run_critic(draft: str) -> str:
    """
    Critic 단계 전체 수행:
    1) Planner의 계획을 바탕으로 프롬프트 구성
    2) Gemini 호출
    3) Critic의 피드백/개선 제안 텍스트 반환
    """
    prompt = build_critic_prompt(draft) # Planner의 계획을 바탕으로 프롬프트 구성
    result = call_gemini(prompt) # Gemini 호출
    return result.strip() # Critic의 피드백/개선 제안 텍스트 반환