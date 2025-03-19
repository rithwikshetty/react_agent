# ReAct Agent

A powerful AI agent that implements the ReAct (Reasoning and Acting) framework using Groq's Llama 3.3 70B model and Tavily for internet searches. This implementation is based on the paper [&#34;ReAct: Synergizing Reasoning and Acting in Language Models&#34;](https://arxiv.org/pdf/2210.03629).

## What is ReAct?

ReAct is a framework that enables language models to reason and act in a structured way to solve complex tasks. It combines reasoning and acting in an interleaved manner, allowing the model to:

1. **Reason**: Think about what to do next
2. **Act**: Take an action to gather information or solve a problem
3. **Observe**: Process the results of the action
4. **Repeat**: Continue this cycle until a solution is found

The key benefits of ReAct include:

- Improved reasoning capabilities through structured thought processes
- Better handling of complex, multi-step tasks
- Enhanced ability to recover from errors
- More transparent decision-making process

## Features

- Implements the ReAct framework with a thought-action-observation loop
- Uses Groq's Llama 3.3 70B model for advanced reasoning
- Performs internet searches using Tavily
- Provides detailed, well-structured answers
- Interactive command-line interface
- Configurable maximum iterations for complex queries

## Architecture

The agent follows the ReAct framework with the following components:

1. **Agent Class**: Manages conversation with the LLM and maintains conversation history
2. **System Prompt**: Guides the LLM's behavior through the ReAct loop
3. **Tools**:
   - Internet search using Tavily API
   - (Extensible for additional tools)
4. **Main Loop**: Implements the ReAct cycle:
   ```
   Thought -> Action -> PAUSE -> Observation -> Thought -> ...
   ```

## Prerequisites

- Python 3.8 or higher
- Groq API key
- Tavily API key

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/react-agent.git
cd react-agent
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:

```bash
cp .env.example .env
```

Then edit the `.env` file with your API keys.

## Usage

You can run the agent in two modes:

### Interactive Mode

Run the agent in interactive mode where you can continuously ask questions:

```bash
python react_agent.py --interactive
# or
python react_agent.py -i
```

In interactive mode:

- Type your questions and press Enter
- Exit by typing 'exit', 'quit', or 'bye'
- Or press Ctrl+C at any time

### Single Query Mode

Run the agent with a single query:

```bash
python react_agent.py --query "What are the best database warehouses in the market?"
```

### Additional Options

- `--max-iterations`: Set the maximum number of iterations (default: 10)
  ```bash
  python react_agent.py --interactive --max-iterations 15
  ```

## Example Output

```
Thought: I need to research current database warehouse solutions...
Action: internet_search: top database warehouses 2024
PAUSE

Observation: [Search results will appear here]

Thought: Now I can analyze the information...
Answer: [Comprehensive answer will appear here]
```

## Implementation Details

The agent is implemented with the following key components:

1. **Agent Class**: Handles the conversation with the LLM and maintains the conversation history
2. **System Prompt**: Implements the ReAct framework with clear instructions for the LLM
3. **Tools**: Currently supports internet search through Tavily API
4. **Main Loop**: Implements the ReAct cycle with configurable iterations
5. **Answer Extraction**: Uses regex to extract the final answer from the conversation

## License

MIT License - feel free to use this project for your own purposes.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
