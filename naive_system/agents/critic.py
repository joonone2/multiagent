# naive_system/agents/critic.py

from naive_system.prompts import CRITIC_SYSTEM_PROMPT
from naive_system.utils.llm_client import call_gemini


def build_critic_prompt(question: str, plan: str, draft: str) -> str:
    # 질문(question), 계획(plan), 초안(draft) 3가지를 모두 조합해서 프롬프트를 만듭니다.
    full_prompt = f"""{CRITIC_SYSTEM_PROMPT}

[사용자 질문]
{question}

[Planner의 기획 의도]
{plan}

[Drafter의 초안]
{draft}
"""
    return full_prompt


def run_critic(question: str, plan: str, draft: str) -> str:
    # 인자를 3개 받도록 수정했습니다.
    prompt = build_critic_prompt(question, plan, draft)
    result = call_gemini(prompt)
    return result.strip()