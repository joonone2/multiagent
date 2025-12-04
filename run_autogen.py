# run_autogen.py

"""
AutoGen 기반 멀티에이전트 시스템 실행 엔트리포인트.

터미널에서:
    python run_autogen.py

로 실행하면,
Debater / Verifier / Moderator가 AutoGen RoundRobinGroupChat으로
질문에 대해 협력적으로 답변을 생성하는 과정을 콘솔에 출력한다.
"""

import asyncio
from autogen_system.workflow import run_autogen_workflow


def main():
    asyncio.run(run_autogen_workflow())


if __name__ == "__main__":
    main()

# hello