# autogen_system/workflow.py
"""
AutoGen 멀티에이전트 워크플로우:
Debater, Verifier, Moderator를 RoundRobinGroupChat으로 묶어서
질문 하나에 대해 협력적으로 답변을 만들어내는 흐름을 정의한다.
"""

from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.messages import TextMessage

from autogen_system.agents import create_debater, create_verifier, create_moderator
from autogen_system.config import create_model_client


MAIN_QUESTION = """
다음 질문에 대해, 핵심 내용을 5문장 이내로 명확하게 설명해주세요:
‘왜 멀티에이전트 시스템이 단일 LLM보다 복잡한 문제 해결에 더 적합할 수 있는가?’
"""


async def run_autogen_workflow(question: str | None = None) -> None:
    """
    AutoGen 기반 멀티에이전트 팀을 구성하고,
    하나의 질문에 대한 협업 대화를 수행한다.
    """
    if question is None:
        question = MAIN_QUESTION.strip()

    # 하나의 model_client를 세 에이전트가 공유
    model_client = create_model_client()

    debater = create_debater(model_client)
    verifier = create_verifier(model_client)
    moderator = create_moderator(model_client)

    # 대화 종료 조건: '최종 답변:'이 언급되거나, 최대 9개의 메시지가 오가면 종료
    termination = TextMentionTermination(text="최종 답변:") | MaxMessageTermination(max_messages=10)

    # 팀 구성: Debater -> Verifier -> Moderator 순환
    team = RoundRobinGroupChat(
        participants=[debater, verifier, moderator],
        termination_condition=termination,
    )

    # TextMessage를 사용해 질문 전달
    task = TextMessage(
        content=(
            "다음 질문에 대해 팀이 협력하여 답변을 만들어주세요.\n\n"
            f"{question}"
        ),
        source="user",
    )

    # 스트리밍 실행
    stream = team.run_stream(task=task)

    await Console(stream)

    # # 🔥 여기서 직접 이벤트를 돌면서 출력 + 히스토리 수집
    # history = []

    # async for event in stream:
    #     # Console 역할 비슷하게 그냥 이벤트 자체를 출력
    #     print(event)

    #     # event 안에 messages가 있을 때만 기록
    #     if hasattr(event, "messages"):
    #         for msg in event.messages:
    #             history.append(msg)

    # === 여기부터 히스토리 한 번 찍어보는 부분 ===
    # print("\n\n===== [FULL CONVERSATION HISTORY] =====")
    # for i, message in enumerate(history):
    #     role = getattr(message, "source", "unknown")
    #     content = getattr(message, "content", "")
    #     print(f"\n--- Message {i} ({role}) ---")
    #     print(content)

    # model_client 정리
    await model_client.close()