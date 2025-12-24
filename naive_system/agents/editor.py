# naive_system/agents/editor.py

from naive_system.prompts import EDITOR_SYSTEM_PROMPT
from naive_system.utils.llm_client import call_gemini

def build_editor_prompt(question: str, draft: str, critique: str) -> str:
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
    # 인자 추가됨: question
    prompt = build_editor_prompt(question, draft, critique)
    result = call_gemini(prompt)
    return result.strip()