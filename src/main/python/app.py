"""
Sample application class for demonstration.
"""
from typing import Optional
from langchain_aws import ChatBedrockConverse
import boto3
import os
import re


class App:
    def __init__(self, name: Optional[str] = None):
        self.model_id = 'us.anthropic.claude-sonnet-4-20250514-v1:0'
        self.region = 'us-east-1'
        self.llm = ChatBedrockConverse(
                model=self.model_id,
                region_name=self.region,
                temperature=0.7,
                max_tokens=1000,
            )
        self.boto_client = boto3.client("bedrock", region_name=self.region)
        interface_functions = self.read_from_source_code('weather_tools.py')
        self.system_prompt = f'''
Your job is to write python function that answers the user’s question. You have the following functions you can call to help provide context, and then you can make one final call to an LLM to produce an answer, given the context. Alternatively, you can just return an answer directly. If answer cannot be obtained, also return that information directly, along with an explanation. Your response should have the following signature:
def answer_user_question(question: str) → str

You have the following functions at your disposal:

{interface_functions}

 Important: only respond in valid python, with the answer_user_question function implementation. Put any comments you may have in the function's return value. Add any import statements before the function definition. Only use features included in python 3, do not import any additional libraries beyond the above functions (no need to import them).   
'''

    def read_from_source_code(self, filename: str) -> str:
        """
        Read source code from a file and trim import statements from the beginning.
        
        Args:
            filename: Name of the file to read (will look in tools/interfaces/)
            
        Returns:
            str: Source code with import statements trimmed
        """
        try:
            # Construct the full path to the file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_dir, 'tools', 'interfaces', filename)
            
            # Read the file content
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Find the line with '''INTERFACE DEFINITIONS''' or similar marker
            start_index = 0
            for i, line in enumerate(lines):
                if 'INTERFACE' in line and ('"""' in line or "'''" in line):
                    start_index = i + 1  # Start from the line after the marker
                    break
            
            # Return the content from after the interface marker
            return ''.join(lines[start_index:])
            
        except FileNotFoundError:
            return f"# Error: Could not find file {filename}"
        except Exception as e:
            return f"# Error reading file {filename}: {str(e)}"

    def clean_llm_output(self, llm_output: str) -> str:
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

    def execute_llm_code(self, llm_output: str, question: str) -> str:
        """
        Execute LLM-generated code with access to weather tools.
        
        Args:
            llm_output: Raw LLM output containing Python code
            question: The question to ask the generated function
            
        Returns:
            Result of executing the code
        """
        try:
            # Import the weather tools implementations
            from tools.implementations.weather_tools_impl import (
                get_user_location,
                get_geo_from_county,
                get_local_weather,
                call_llm
            )
            from tools.interfaces.weather_tools import Weather
            
            # Clean the LLM output
            cleaned_code = self.clean_llm_output(llm_output)
            
            # Append code to automatically call the function and store result
            runner_code = f"""
# Auto-generated runner code
if 'answer_user_question' in locals():
    _user_question = {repr(question)}
    _function_result = answer_user_question(_user_question)
else:
    _function_result = "Error: No 'answer_user_question' function found in the generated code."
"""
            
            # Combine the cleaned code with the runner
            full_code = cleaned_code + runner_code
            
            # Create a namespace with the weather tools available
            namespace = {
                'get_user_location': get_user_location,
                'get_geo_from_county': get_geo_from_county,
                'get_local_weather': get_local_weather,
                'call_llm': call_llm,
                'Weather': Weather,
                '__builtins__': __builtins__
            }
            
            # Execute the full code in the namespace
            exec(full_code, namespace)
            
            # Return the result stored by the runner
            return str(namespace.get('_function_result', 'Error: No result generated'))
                
        except Exception as e:
            return f"Error executing LLM code: {str(e)}"

    def answer(self, message: str) -> str:
        # Get the LLM response
        llm_response = self.answer_with_prompt(self.system_prompt, message)

        print(f"LLM responded with: {llm_response}")
        
        # Execute the LLM-generated code and return the result
        return self.execute_llm_code(llm_response, message)
    
    def answer_with_prompt(self, system_prompt: str, message: str = "Provide answer to my request, given the context above.") -> str:
    
        try:
            # Python does not support traditional method overloading by argument signature.
            # Defining multiple methods with the same name in a class will override previous definitions.
            from langchain_core.messages import HumanMessage, SystemMessage
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=message)
            ]
            
            # Invoke the model with messages
            response = self.llm.invoke(messages)
            
            # Extract the content from the response
            if hasattr(response, 'content'):
                content = response.content
                if isinstance(content, str):
                    return content
                elif isinstance(content, list):
                    # Handle list of content parts
                    return " ".join(str(part) for part in content)
                else:
                    return str(content)
            else:
                return str(response)
                
        except Exception as e:
            raise Exception(f"Error calling Bedrock LLM with system prompt: {str(e)}")
