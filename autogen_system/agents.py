# autogen_system/agents.py

"""
AutoGen 에이전트 정의:
- Debater: 멀티에이전트의 장점을 설명하는 초안 생성
- Verifier: 초안을 검증하고 논리/내용 피드백
- Moderator: 대화 흐름 관리 + 최종 답변 정리 유도
"""

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

from autogen_system.config import create_model_client


def create_debater(model_client: OpenAIChatCompletionClient | None = None) -> AssistantAgent:
    if model_client is None:
        model_client = create_model_client()

    system_message = (
    "당신은 Debater입니다.\n"
    "- 첫 번째 발언에서는 질문에 대한 3~5문장 초안을 작성하십시오.\n"
    "- 두 번째 발언에서는 Moderator가 요청할 때만 보완 내용을 반영해 수정본을 제시하십시오.\n"
    "- Moderator가 요청하지 않으면 절대 스스로 보완하지 마십시오.\n"
    "- 절대로 글 전체를 다시 구성하거나 장황하게 작성하지 마십시오.\n"
    "- 당신의 역할은 '초안 생성'과 '필요 시 단 1회 수정'입니다."
    )

    agent = AssistantAgent(
        name="debater",
        model_client=model_client,
        system_message=system_message,
    )
    return agent


def create_verifier(model_client: OpenAIChatCompletionClient | None = None) -> AssistantAgent:
    if model_client is None:
        model_client = create_model_client()

    system_message = (
    "당신은 Verifier입니다.\n"
    "- Debater의 초안을 빠르게 검토한 뒤, 다음 두 가지 중 하나만 한 줄로 답하십시오.\n"
    "  1) '좋습니다. 그대로 진행해도 됩니다.'\n"
    "  2) '여기 부분을 한 문장 정도 보완하면 좋겠습니다: ...'\n"
    "- 초안에 조금이라도 더 구체적이거나 명확해질 여지가 있다면, 2번 형태를 사용하십시오.\n"
    "- 1번(그대로 진행) 형태는 정말로 더 고칠 부분이 거의 없다고 판단될 때에만 사용하십시오.\n"
    "- 절대 두 줄 이상 작성하지 말고, 재작성이나 긴 피드백, 요약, 목록, 예시는 제공하지 마십시오.\n"
    "- 당신의 기본 역할은 '부족한 부분을 콕 집어서 보완을 유도하는 것'이며, 승인(1번)은 예외적인 경우입니다."
    )
    agent = AssistantAgent(
        name="verifier",
        model_client=model_client,
        system_message=system_message,
    )
    return agent


def create_moderator(model_client: OpenAIChatCompletionClient | None = None) -> AssistantAgent:
    if model_client is None:
        model_client = create_model_client()

    system_message = (
    "당신은 Moderator입니다.\n"
    "- Verifier가 '보완'을 요청하면 Debater에게 수정 요청을 하십시오.\n"
    "- Verifier가 '좋습니다'라고 하면 최종 답변을 생성하십시오.\n"
    "- 최종 답변은 반드시 '최종 답변:'으로 시작하는 4~6문장입니다.\n"
    "- 최종 답변을 생성한 후에는 추가 발언 금지.\n"
    "- 당신의 목적은 팀 논의를 정리하여 최종 답변을 생성하는 것입니다."
    )
    agent = AssistantAgent(
        name="moderator",
        model_client=model_client,
        system_message=system_message,
    )
    return agent



def create_moderator_consensus(model_client=None):
    if model_client is None:
        model_client = create_model_client()

    system_message = (
        "당신은 Moderator입니다.\n"
        "- Debater_A와 Debater_B가 제출한 두 개의 초안을 비교하여 핵심 내용을 종합하십시오.\n"
        "- 두 초안에서 가장 중요한 논지와 장점을 추려 하나의 일관된 답변으로 재구성하십시오.\n"
        "- 최종 답변은 반드시 '최종 답변:'으로 시작하는 4~6문장 한국어 문단이어야 합니다.\n"
        "- 중복된 내용은 제거하고 핵심 논지를 명확하게 정리하십시오.\n"
        "- 최종 답변을 출력한 뒤에는 추가 발언을 하지 마십시오."
    )

    return AssistantAgent(
        name="moderator",
        model_client=model_client,
        system_message=system_message,
    )