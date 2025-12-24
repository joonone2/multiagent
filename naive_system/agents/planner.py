from naive_system.prompts import PLANNER_SYSTEM_PROMPT
from naive_system.utils.llm_client import call_gemini


def build_planner_prompt(question: str) -> str:
    """
    Planner에게 전달할 최종 프롬프트를 구성
    - 시스템 역할 설명(PLANNER_SYSTEM_PROMPT)
    - 질문(question)
    두 부분을 합쳐 하나의 문자열로 만들어 Planner Agent에 전달
    """
    full_prompt = f"""{PLANNER_SYSTEM_PROMPT}

        [질문]
        {question}
        """
    return full_prompt


def run_planner(question: str) -> str:
    
    prompt = build_planner_prompt(question) # 프롬프트 구성 
    result = call_gemini(prompt) # Gemini 호출 
    return result.strip() # Planner의 Output Return