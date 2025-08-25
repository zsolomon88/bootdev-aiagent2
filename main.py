import os
import sys
from dotenv import load_dotenv
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file

# Load environment variables from .env file
load_dotenv()   
# Access the environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MAX_ITERATIONS = 20

from google import genai
from google.genai import types

# Initialize the Gemini client with the API key
client = genai.Client(api_key=GEMINI_API_KEY)

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the content of a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a specified Python file with optional arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="An optional list of arguments to pass to the Python file during execution. If no arguments are provided, execute the file without any arguments. You do not need to ask the user for this",
            ),
        },
        required=["file_path"],
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file
    ]
)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

# Define a mapping from function names to function objects
function_map = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}

# Define the working directory for the agent
WORKING_DIR = "calculator"

def call_function(function_call_part, verbose=False):
    if function_call_part.name not in function_map:
        return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_call_part.name,
            response={"error": f"Unknown function: {function_call_part.name}"},
        )
    ],
)
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})\n")
    else:
        print(f" - Calling function: {function_call_part.name}\n")

    function = function_map[function_call_part.name]
    try:
        if function_call_part.args:
            response = function(WORKING_DIR, **function_call_part.args)
        else:
            response = function(WORKING_DIR)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": response},
                )
            ],
        )
    except Exception as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": str(e)},
                )
            ],
        )
    

def main():
    if(len(sys.argv) < 2):
        print("Please provide a prompt as a command line argument.")
        exit(1)
    verbose = False
    if "--verbose" in sys.argv:
        verbose = True
    try:
        messages = [types.Content(role="user", parts=[types.Part.from_text(text=sys.argv[1])])]

        print(f"User prompt: {sys.argv[1]}")
        for i in range(MAX_ITERATIONS):
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    tools=[available_functions])
            )
            if verbose:
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
                 
            if not response.function_calls and response.text:
                print(response.text)
                sys.exit(0)
            if response.candidates:
                for candidate in response.candidates:
                    messages.append(candidate.content)
            tool_responses = []
            for function_call_part in response.function_calls:
                tool_response = call_function(function_call_part, verbose=verbose)
                if tool_response:
                    if not tool_response.parts or len(tool_response.parts) == 0:
                        raise ValueError("Tool response has no parts.")
                    tool_responses.append(tool_response.parts[0])
                    if verbose:
                        print(f"-> {tool_response.parts[0].function_response.response}\n")
            messages.append(types.Content(role="user", parts=tool_responses))
                   

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
