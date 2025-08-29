# LLM Tool Calling

Demonstrate code-first tool calling. LLM is able to call multiple tools in one shot, and generate a program to gather and produce data necessary to answer user query. This is similar to smolagents (but completely insecure, so just useful to study the mechanism), but very different from how most other frameworks call tools (one tool at a time).

In the demo, we have purposefully incompatible weather tools, so that multiple calls need to be made in order to figure out local weather. The LLM has the following options:
- answer cannot be provided (what do I have in my pocket?)
- answer can be provided without calling any tools (what is the capital of Indonesia?)
- answer can be provided with a single tool call (what state am I in?)
- answer requires tool calls to be chained (what is the temperature outside?)
- answer requires multiple tools to be called and interpreted by the LLM (what should I wear today?)

The reason that this approach works well is that LLMs are already good at writing code, and can figure in one shot how to arrange the tool calls and manipulate the data structures to get at a desired answer. I created this when I noticed the default tool calling mechanism in LangChain was way too complicated (ironically, this still uses LangChain to talk to AWS Bedrock). Meanwhile a smaller, less known framework, smolagents, does this by default. 

## Prerequisites

- [uv](https://docs.astral.sh/uv/) - Python package manager
- AWS credentials configured for Bedrock access (AWS_* environment variables or ~/.aws/config file, as per boto3 auth mechanism)

## Setup and Running

After checking out the project:

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Run the application:**
   ```bash
   uv run python -m main "what should I wear today?"
   uv run python -m main "what is the temperature outside?"
   uv run python -m main "what state am I in?"
   uv run python -m main "what is the capital of Indonesia?"
   ```

## Running Tests

To run the integration tests that validate the LLM tool calling functionality:

```bash
uv run python -m unittest src.test.python.test_app -v
```

## License

MIT License