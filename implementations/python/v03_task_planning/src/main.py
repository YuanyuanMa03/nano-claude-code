"""Main entry point for v03 task planning."""

import os
import sys
from dotenv import load_dotenv

# Import with fallback for different execution contexts
try:
    from .agent import AgentLoop
except ImportError:
    from agent import AgentLoop

# Load environment variables
load_dotenv()


def main():
    """Main entry point."""
    # Get API key from environment
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        print("Please set it in your .env file or environment")
        sys.exit(1)

    # Get model from environment (optional)
    model = os.getenv("MODEL_ID", "claude-sonnet-4-6")

    # Get workspace from environment (optional)
    workspace = os.getenv("WORKSPACE", ".")

    # Initialize agent
    agent = AgentLoop(api_key=api_key, model=model, workspace=workspace)

    # Interactive loop
    print("nano-claude-code v03 - Task Planning")
    print(f"Workspace: {os.path.abspath(workspace)}")
    print(f"Tools: {', '.join(agent.list_tools())}")
    print("\nMotto: \"An agent without a plan drifts\"")
    print("Type 'exit' or 'quit' to exit")
    print("-" * 50)

    while True:
        try:
            # Get user input
            user_input = input("\nYou: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break

            # Run agent
            print("\nAgent: ", end="", flush=True)
            response = agent.run(user_input)
            print(response)

            # Show todo stats if any todos
            stats = agent.get_todo_stats()
            if stats["total"] > 0:
                print(f"\n[Todo Progress: {stats['completed']}/{stats['total']} completed]")

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")


if __name__ == "__main__":
    main()
