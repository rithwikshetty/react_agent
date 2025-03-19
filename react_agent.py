#!/usr/bin/env python3
# This script implements a ReAct (Reasoning and Acting) agent using Groq LLM and Tavily search API
import os
import sys
import argparse
from dotenv import load_dotenv
from groq import Groq
from tavily import TavilyClient
import re

# Load environment variables from .env file
load_dotenv()

# Check for required environment variables
required_env_vars = ["GROQ_API_KEY", "TAVILY_API_KEY"]
missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
    print("Please set them in your .env file")
    sys.exit(1)

# Initialize API clients
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
tavily_client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))

class Agent:
    """
    Agent class that manages conversation with the LLM and maintains conversation history
    """
    def __init__(self, client, system_prompt):
        """
        Initialize the agent with an LLM client and system prompt
        
        Args:
            client: The LLM client (Groq)
            system_prompt: The system prompt to guide the LLM's behavior
        """
        self.client = client
        self.system_prompt = system_prompt
        self.messages = []

        # Add system prompt to conversation history if provided
        if self.system_prompt is not None:
            self.messages.append({"role": "system", "content": self.system_prompt})

    def __call__(self, message=""):
        """
        Send a message to the LLM and get a response
        
        Args:
            message: The user message to send to the LLM
            
        Returns:
            The LLM's response
        """
        if message:
            self.messages.append({"role": "user", "content": message})

        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result

    def execute(self):
        """
        Execute the LLM call with the current conversation history
        
        Returns:
            The LLM's response or an error message
        """
        try:
            completion = self.client.chat.completions.create(
                messages=self.messages,
                model="llama-3.3-70b-versatile",
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Error during API call: {str(e)}")
            return "Error: Failed to get response from the model."

def internet_search(query):
    """
    Perform an internet search using Tavily API
    
    Args:
        query: The search query
        
    Returns:
        The search results as a string or an error message
    """
    try:
        response = tavily_client.search(query, max_results=2)
        response_content = "\n".join([result["content"] for result in response["results"]])
        return response_content
    except Exception as e:
        print(f"Error during internet search: {str(e)}")
        return "Error: Failed to perform internet search."

def agent_loop(max_iterations, query, system_prompt):
    """
    Run the agent in a loop until it produces an answer or reaches max iterations
    
    Args:
        max_iterations: Maximum number of iterations to run
        query: The initial user query
        system_prompt: The system prompt for the agent
        
    Returns:
        The conversation history
    """
    agent = Agent(client, system_prompt)
    i = 0
    while i < max_iterations:
        i += 1
        result = agent(query)
        print(result)
        # Break the loop if an answer is found
        if re.search(r"Answer:.*", result):
            break
    return agent.messages

def extract_answer(messages):
    """
    Extract the final answer from the conversation history
    
    Args:
        messages: The conversation history
        
    Returns:
        The extracted answer or an error message
    """
    if not messages:
        return "No messages found."
    
    answer_text = messages[-1]['content']
    match = re.search(r'Answer:(.*?)(?=$)', answer_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return "No answer found in the output."

def process_query(query, system_prompt, max_iterations=10):
    """
    Process a user query through the agent and display the final answer
    
    Args:
        query: The user query
        system_prompt: The system prompt for the agent
        max_iterations: Maximum number of iterations to run
    """
    try:
        output = agent_loop(max_iterations, query=query, system_prompt=system_prompt)
        final_answer = extract_answer(output)
        print("\nFinal Answer:")
        print(final_answer)
        print("\n" + "="*80 + "\n")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("\n" + "="*80 + "\n")

def display_banner():
    """
    Display a stylized ASCII art banner for ReAct Agent
    """
    banner = """
██████╗ ███████╗ █████╗  ██████╗████████╗
██╔══██╗██╔════╝██╔══██╗██╔════╝╚══██╔══╝
██████╔╝█████╗  ███████║██║        ██║   
██╔══██╗██╔══╝  ██╔══██║██║        ██║   
██║  ██║███████╗██║  ██║╚██████╗   ██║   
╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝   ╚═╝   
                                          
 █████╗  ██████╗ ███████╗███╗   ██╗████████╗
██╔══██╗██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝
███████║██║  ███╗█████╗  ██╔██╗ ██║   ██║   
██╔══██║██║   ██║██╔══╝  ██║╚██╗██║   ██║   
██║  ██║╚██████╔╝███████╗██║ ╚████║   ██║   
╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝   
"""
    print("\033[38;5;208m" + banner + "\033[0m")  # Print in a coral/orange color similar to the image

def main():
    """
    Main function to parse arguments and run the agent
    """
    parser = argparse.ArgumentParser(description='React Agent - An AI agent that uses Groq and Tavily')
    parser.add_argument('--query', help='Single query to process (optional)')
    parser.add_argument('--max-iterations', type=int, default=10, help='Maximum number of iterations (default: 10)')
    parser.add_argument('--interactive', '-i', action='store_true', help='Run in interactive mode')
    args = parser.parse_args()

    # Define the system prompt that guides the agent's behavior
    system_prompt = """
    You run in a loop of Thought, Action, PAUSE, Observation.
    At the end of the loop you output an Answer
    Use Thought to describe your thoughts about the question you have been asked.
    Use Action to run one of the actions available to you - then return PAUSE.
    Observation will be the result of running those actions.

    Your available actions are:

    internet_search:
    e.g. internet_search: current population of France
    Searches the internet and returns relevant information about the query

    Example session:

    Question: What are the key differences between React and Angular for modern web development?
    Thought: I need to research the main differences between React and Angular frameworks.
    Action: internet_search: key differences between React and Angular 2023
    PAUSE 

    You will be called again with this:

    Observation: React is a JavaScript library focused on UI components with a virtual DOM for efficient rendering. Angular is a complete TypeScript-based framework with two-way data binding. React has a smaller learning curve and more flexibility, while Angular provides more built-in functionality and enforces stricter patterns. React uses JSX, while Angular uses templates with directives. React's performance is generally better for dynamic content, while Angular excels in large enterprise applications.

    Thought: I should get more specific information about their architecture and state management.
    Action: internet_search: React vs Angular architecture and state management
    PAUSE

    You will be called again with this: 

    Observation: React uses a one-way data flow and relies on external libraries like Redux or Context API for state management. Angular has built-in services and dependency injection with NgRx for state management. React's component-based architecture is more flexible but requires additional libraries for routing and HTTP requests. Angular's comprehensive framework includes Angular Router and HttpClient. React's virtual DOM offers performance advantages for frequent UI updates, while Angular's change detection can be less efficient but more predictable.

    Thought: I should also look into developer experience and community support.
    Action: internet_search: React vs Angular developer experience and community trends 2023
    PAUSE

    You will be called again with this:

    Observation: React has a larger community with 197k GitHub stars compared to Angular's 86k. React's npm downloads are significantly higher. React's ecosystem is more diverse but fragmented, requiring developers to make more architectural decisions. Angular provides a more standardized approach with official libraries. React's job market is larger, but Angular developers often command higher salaries. React is favored by startups and tech companies, while Angular is more common in enterprise environments. React's documentation is good but community-dependent, while Angular offers comprehensive official documentation.

    If you have the answer, output it as the Answer.

    Answer: React and Angular represent two different approaches to web development. React is a lightweight library focused on UI components with a virtual DOM, one-way data binding, and a flexible ecosystem that requires additional libraries for full functionality. It has a larger community, more GitHub stars, and higher npm downloads, making it popular among startups and tech companies. Angular is a comprehensive TypeScript framework with two-way data binding, built-in services, dependency injection, and includes everything needed for large applications. It enforces stricter patterns and is favored in enterprise environments. React generally offers better performance for dynamic content with its virtual DOM, while Angular provides more structure and built-in functionality at the cost of a steeper learning curve. Your choice should depend on project requirements, team expertise, and organizational needs.

    Important instructions:
    1. Approach each question from multiple angles and perspectives
    2. Consider various stakeholders and use cases in your analysis
    3. When you receive search results, use them to formulate additional questions that explore related aspects
    4. Your final answer should be comprehensive and in-depth, covering:
       - Main factual information
       - Different perspectives on the topic
       - Potential implications or applications
       - Nuances and edge cases
       - Recommendations when appropriate
    5. Don't rush to a conclusion - explore the topic thoroughly before providing your final answer

    Now it's your turn:
    """.strip()

    # Handle different execution modes
    if args.interactive:
        # Interactive mode - continuously prompt for user questions
        display_banner()
        print("\nWelcome to ReAct Agent! Ask me anything...")
        print("\nType 'exit', 'quit', or 'bye' to end the session")
        print("Press Ctrl+C to exit at any time")
        print("\n" + "="*80 + "\n")
        try:
            while True:
                query = input("\033[1mYour question:\033[0m ").strip()  # Make the prompt bold
                if query.lower() in ['exit', 'quit', 'bye']:
                    print("\nThank you for using ReAct Agent. Goodbye!")
                    break
                if query:
                    process_query(query, system_prompt, args.max_iterations)
        except KeyboardInterrupt:
            print("\nThank you for using ReAct Agent. Goodbye!")
    elif args.query:
        # Single query mode - process one query and exit
        display_banner()
        process_query(args.query, system_prompt, args.max_iterations)
    else:
        # No arguments provided - show help
        display_banner()
        parser.print_help()

# Entry point of the script
if __name__ == "__main__":
    main() 