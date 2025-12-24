import asyncio
import logging


from autogen_system.workflow_selector import run_selector_workflow


def main() -> None:
    asyncio.run(run_selector_workflow())


if __name__ == "__main__":
    main()                                  