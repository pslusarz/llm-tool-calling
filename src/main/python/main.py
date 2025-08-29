"""
Main application module for llm-tool-calling.
"""
import sys
from app import App


def main():
    """Main entry point for the application."""
    # Get question from command line args or use default
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
    else:
        question = "what should I wear today?"
    
    # Create and run the app
    app = App()
    answer = app.answer(question)
    print(f"Answer: {answer}")

    
 


if __name__ == "__main__":
    main()
