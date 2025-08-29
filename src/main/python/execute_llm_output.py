#!/usr/bin/env python3
"""
Execute LLM-generated code with access to weather tools implementations.
"""
import sys
import os
import re

# Import the weather tools implementations to make them available
from tools.implementations.weather_tools_impl import (
    get_user_location,
    get_geo_from_county,
    get_local_weather,
    call_llm
)
from tools.interfaces.weather_tools import Weather

def clean_llm_output(llm_output: str) -> str:
    """
    Clean the LLM output by removing markdown code blocks and standalone 'python' lines.
    
    Args:
        llm_output: Raw LLM output string
        
    Returns:
        Cleaned Python code string
    """
    # Remove markdown code blocks
    code = re.sub(r'```python\n?', '', llm_output)
    code = re.sub(r'```\n?', '', code)
    
    # Remove standalone 'python' lines
    lines = code.split('\n')
    cleaned_lines = []
    
    for line in lines:
        stripped = line.strip()
        # Skip lines that are just 'python' or variations
        if stripped.lower() in ['python', 'python3', '>>> python', '$ python']:
            continue
        cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)

def execute_llm_code(llm_output: str, question: str = "What's the temperature outside?") -> str:
    """
    Execute LLM-generated code with access to weather tools.
    
    Args:
        llm_output: Raw LLM output containing Python code
        question: The question to ask the generated function
        
    Returns:
        Result of executing the code
    """
    try:
        # Clean the LLM output
        cleaned_code = clean_llm_output(llm_output)
        
        # Create a namespace with the weather tools available
        namespace = {
            'get_user_location': get_user_location,
            'get_geo_from_county': get_geo_from_county,
            'get_local_weather': get_local_weather,
            'call_llm': call_llm,
            'Weather': Weather,
            '__builtins__': __builtins__
        }
        
        # Execute the cleaned code in the namespace
        exec(cleaned_code, namespace)
        
        # Try to find and call the answer_user_question function
        if 'answer_user_question' in namespace:
            result = namespace['answer_user_question'](question)
            return str(result)
        else:
            return "Error: No 'answer_user_question' function found in the generated code."
            
    except Exception as e:
        return f"Error executing LLM code: {str(e)}"

def main():
    """
    Main function to demonstrate usage.
    """
    print("LLM Code Executor")
    print("=" * 50)
    
    # Example: Get LLM output from user input or file
    print("Please paste the LLM output (end with 'END' on a new line):")
    
    lines = []
    while True:
        try:
            line = input()
            if line.strip() == 'END':
                break
            lines.append(line)
        except EOFError:
            break
    
    llm_output = '\n'.join(lines)
    
    if llm_output.strip():
        question = input("\nEnter your question (or press Enter for default): ").strip()
        if not question:
            question = "What's the temperature outside?"
        
        print(f"\nExecuting LLM code for question: {question}")
        print("-" * 50)
        
        result = execute_llm_code(llm_output, question)
        print(f"Result: {result}")
    else:
        print("No LLM output provided.")

if __name__ == "__main__":
    main()
