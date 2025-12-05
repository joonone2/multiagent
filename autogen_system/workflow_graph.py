# autogen_system/workflow_graph.py
"""
GraphFlow 기반 멀티에이전트 워크플로우
구조:

  [manager_start]
        |
        v
 [expert_structure]   [expert_example]   [expert_limits]
        \                |                /
         \               |               /
          \              v              /
              [manager_final]

- 에이전트 생성은 여기 파일 안에서 직접 AssistantAgent로 정의.
- 기존 Debater/Verifier/Moderator 코드는 그대로 둔다 (사용 안 함).
"""

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import DiGraphBuilder, GraphFlow
from autogen_agentchat.ui import Console
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination

from autogen_system.config import create_model_client


MAIN_QUESTION = """
다음 질문에 대해, 핵심 내용을 5문장 이내로 명확하게 설명해주세요:
‘왜 멀티에이전트 시스템이 단일 LLM보다 복잡한 문제 해결에 더 적합할 수 있는가?’
""".strip()


async def run_graph_workflow(question: str | None = None) -> None:
    """
    manager_start → (expert_structure, expert_example, expert_limits) → manager_final
    구조의 GraphFlow 워크플로우를 실행한다.
    """
    if question is None:
        question = MAIN_QUESTION

    # 1) 공용 모델 클라이언트 생성 (Gemini 래핑하는 기존 함수 그대로 사용)
    model_client = create_model_client()

    # 2) 에이전트 정의 ──────────────────────────────────────
    manager_start = AssistantAgent(
        name="manager_start",
        model_client=model_client,
        system_message=(
            "당신은 팀 리더(manager_start)입니다.\n"
            "- 사용자의 질문을 1~2문장으로 짧게 요약하세요.\n"
            "- 그리고 세 명의 전문가가 어떤 관점에서 답하면 좋을지 역할을 배분해 주세요.\n"
            "  * expert_structure: 구조/시스템 관점\n"
            "  * expert_example: 직관적인 예시/사례 관점\n"
            "  * expert_limits: 단일 LLM의 한계 및 비교 관점\n"
            "- 각 전문가에게 '당신은 ○○ 관점만 다뤄주세요'처럼 간단히 지시하세요.\n"
            "- 직접 최종 답변을 만들지 말고, 자신의 짧은 의견 1문장만 덧붙인 뒤 전문가들을 기다리세요."
        ),
    )

    expert_structure = AssistantAgent(
        name="expert_structure",
        model_client=model_client,
        system_message=(
            "당신은 '구조/시스템 관점' 전문가(expert_structure)입니다.\n"
            "- 멀티에이전트 시스템의 구조적 장점(역할 분리, 병렬 처리, 협력 구조 등)을 중심으로 설명하세요.\n"
            "- 단일 LLM과 비교했을 때 복잡한 문제를 어떻게 더 잘 쪼개고 처리할 수 있는지 3~4문장으로 정리하세요.\n"
            "- 오직 구조/시스템 관점만 다루고, 예시를 길게 풀거나 단일 LLM의 한계를 자세히 분석하는 역할은 다른 전문가에게 맡기세요.\n"
            "- 다른 전문가(expert_example, expert_limits)의 역할을 대신 설명하지 마십시오."
        ),
    )


    expert_example = AssistantAgent(
        name="expert_example",
        model_client=model_client,
        system_message=(
            "당신은 '예시/직관' 전문가(expert_example)입니다.\n"
            "- 멀티에이전트 시스템이 유리한 실제 또는 가상의 예시를 1~2개 들어 설명하세요.\n"
            "- 예시는 자율주행, 협업 에이전트, 소프트웨어 개발, 멀티에이전트 회의 등 직관적인 사례 위주로 드세요.\n"
            "- 전체는 3~5문장 이내로 유지하세요.\n"
            "- 구조적인 이론 설명이나 단일 LLM의 한계를 깊게 분석하는 것은 다른 전문가에게 맡기고, 당신은 이해를 돕는 사례 설명에만 집중하세요."
        ),
    )

    expert_limits = AssistantAgent(
        name="expert_limits",
        model_client=model_client,
        system_message=(
            "당신은 '단일 LLM의 한계/비교' 전문가(expert_limits)입니다.\n"
            "- 단일 LLM이 복잡한 문제에서 가지는 한계(맥락 길이, 단일 관점, 도메인 특화 부족 등)를 2~3문장으로 짚어주세요.\n"
            "- 그리고 멀티에이전트가 그 한계를 어떻게 보완하는지 2~3문장으로 설명하세요.\n"
            "- 전체는 4~6문장 이내로 작성하세요.\n"
            "- 구조적인 상세 설계나 구체적인 사례 설명은 다른 전문가가 맡으므로, 여기서는 '비교와 한계'에만 집중하세요."
        ),
    )

    manager_final = AssistantAgent(
        name="manager_final",
        model_client=model_client,
        system_message=(
            "당신은 최종 정리자(manager_final)입니다.\n"
            "- manager_start, expert_structure, expert_example, expert_limits의 발언을 모두 참고해 주세요.\n"
            "- 사용자의 질문에 대한 최종 답변을 4~5문장짜리 한국어 문단으로 작성하세요.\n"
            "- 반드시 '최종 답변:'으로 시작해야 합니다.\n"
            "- 새로운 논의를 시작하지 말고, 앞에서 나온 핵심 논점을 요약·통합하는 데 집중하세요.\n"
            "- 최종 답변을 한 번 출력한 뒤에는 추가 발언을 하지 마세요."
        ),
    )

    # 3) 그래프 정의 (manager_start → 3 expert → manager_final) ─────────────
    builder = DiGraphBuilder()

    (
        builder.add_node(manager_start)
        .add_node(expert_structure)
        .add_node(expert_example)
        .add_node(expert_limits)
        .add_node(manager_final)
    )

    # manager_start → 세 expert (fan-out)
    builder.add_edge(manager_start, expert_structure)
    builder.add_edge(manager_start, expert_example)
    builder.add_edge(manager_start, expert_limits)

    # 세 expert → manager_final (fan-in)
    # activation_group을 주지 않아도,
    # 각 expert 발화 이후 manager_final이 후보로 올라오고,
    # '최종 답변:'을 출력하면 termination 조건으로 종료됨.
    builder.add_edge(expert_structure, manager_final)
    builder.add_edge(expert_example, manager_final)
    builder.add_edge(expert_limits, manager_final)

    graph = builder.build()

    # 4) 종료 조건 ─────────────────────────────────────────
    termination = TextMentionTermination(text="최종 답변:") | MaxMessageTermination(
        max_messages=20
    )

    # 5) GraphFlow 팀 구성 ─────────────────────────────────
    flow = GraphFlow(
        participants=builder.get_participants(),  # [manager_start, expert_*, manager_final]
        graph=graph,
        termination_condition=termination,
    )

    # 6) 시작 task: manager_start가 먼저 팀에게 브리핑하도록 함 ─────────────
    task = (
        "다음은 사용자가 제시한 질문입니다. 팀이 협력하여 답변을 만들어 주세요.\n\n"
        f"[사용자 질문]\n{question}\n"
    )

    # writer 예제처럼 문자열 그대로 넘기면, 첫 노드는 manager_start가 담당하게 됨
    stream = flow.run_stream(task=task)

    # 7) 콘솔에 대화 내용을 순서대로 출력
    await Console(stream)

    # 8) 리소스 정리
    await model_client.close()