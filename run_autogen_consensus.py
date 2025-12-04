import asyncio
from autogen_system.workflow_consensus import run_consensus_workflow

def main():
    asyncio.run(run_consensus_workflow())

if __name__ == "__main__":
    main()