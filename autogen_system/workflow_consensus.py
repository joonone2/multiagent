# autogen_system/workflow_consensus.py

"""
Consensus 기반 멀티에이전트 워크플로우.

- Debater_A, Debater_B: 같은 역할 설명을 가진 두 명의 디베이터
- Moderator: 두 답변을 읽고 최종 합의 답변을 만드는 에이전트

흐름:
User 질문
  → Debater_A: 초안 1
  → Debater_B: 초안 2
  → Moderator: 두 초안을 종합해서 '최종 답변:' 한 번 출력하고 종료
"""

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.messages import TextMessage

from autogen_system.config import create_model_client


MAIN_QUESTION = """
다음 질문에 대해, 핵심 내용을 5문장 이내로 명확하게 설명해주세요:
‘왜 멀티에이전트 시스템이 단일 LLM보다 복잡한 문제 해결에 더 적합할 수 있는가?’
"""


async def run_consensus_workflow(question: str | None = None) -> None:
    if question is None:
        question = MAIN_QUESTION.strip()

    # 공용 모델 클라이언트 (Gemini)
    model_client = create_model_client()

    # 🔹 Debater용 시스템 메시지 (두 명이 똑같이 공유)
    debater_system_message = (
        "당신은 Debater입니다. 사용자의 질문에 대해 자신의 관점에서 답변을 제시하는 역할입니다.\n"
        "- 멀티에이전트 시스템과 단일 LLM을 비교하여, 왜 멀티에이전트가 복잡한 문제에 더 적합할 수 있는지 설명하십시오.\n"
        "- 답변은 4~6문장 정도의 한국어 문단으로 간결하게 작성하십시오.\n"
        "- 다른 에이전트의 존재를 언급하지 말고, 오직 자신의 관점에서만 논리를 전개하십시오.\n"
        "- 불필요하게 장황하게 쓰지 말고, 핵심 논리를 명확하게 전달하십시오."
    )

    # 🔹 Moderator(합의자)용 시스템 메시지
    moderator_system_message = (
        "당신은 Moderator입니다.\n"
        "- Debater_A와 Debater_B가 제시한 두 개의 답변 초안을 읽고, 핵심 내용을 종합하십시오.\n"
        "- 두 초안에서 중요한 논지를 추려 중복을 제거하고, 하나의 일관된 답변으로 재구성하십시오.\n"
        "- 최종 답변은 반드시 '최종 답변:'으로 시작하는 4~6문장 한국어 문단이어야 합니다.\n"
        "- 어느 디베이터가 무엇을 말했다는 메타 코멘트는 쓰지 말고, 통합된 관점에서만 작성하십시오.\n"
        "- 최종 답변을 출력한 뒤에는 추가 발언을 하지 마십시오."
    )

    # 🔹 Debater 두 명 (이름만 다르고, 같은 프롬프트/모델 사용)
    debater_a = AssistantAgent(
        name="Debater_A",
        model_client=model_client,
        system_message=debater_system_message,
    )

    debater_b = AssistantAgent(
        name="Debater_B",
        model_client=model_client,
        system_message=debater_system_message,
    )

    # 🔹 Moderator 에이전트
    moderator = AssistantAgent(
        name="moderator",
        model_client=model_client,
        system_message=moderator_system_message,
    )

    # 🔹 종료 조건: '최종 답변:' 등장 or 메시지 10개 초과
    termination = TextMentionTermination("최종 답변:") | MaxMessageTermination(10)

    # 🔹 팀 구성: Debater_A → Debater_B → moderator
    team = RoundRobinGroupChat(
        participants=[debater_a, debater_b, moderator],
        termination_condition=termination,
    )

    # 🔹 사용자 질문 전달
    task = TextMessage(
        content=(
            "Debater_A와 Debater_B는 각각 독립적으로 답변 후보를 제시하고, "
            "moderator는 두 답변을 종합하여 최종 답변을 작성해 주세요.\n\n"
            f"{question}"
        ),
        source="user",
    )

    # 🔹 스트리밍 실행 + 콘솔 출력
    stream = team.run_stream(task=task)
    await Console(stream)

    # 🔹 리소스 정리
    await model_client.close()