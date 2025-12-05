# run_autogen_graph.py
import asyncio
from autogen_system.workflow_graph import run_graph_workflow


def main() -> None:
    asyncio.run(run_graph_workflow())


if __name__ == "__main__":
    main()