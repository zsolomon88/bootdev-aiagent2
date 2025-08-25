import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Validate that the full path is not outside the working directory
    if not full_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory\n'
    
    if not os.path.isfile(full_path):
        return f'Error: File "{file_path}" not found.\n'
    
    if not full_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.\n'
    try:
        command = ['python', full_path] + args
        completed_process = subprocess.run(command, capture_output=True, text=True, timeout=30) 
        output = completed_process.stdout
        error = completed_process.stderr
        final_output = ""
        if output:
            final_output += f'STDOUT:{output}\n'
        else:
            final_output += "No output produced.\n"
        if error:
            final_output += f'STDERR:{error}\n'

        if completed_process.returncode != 0:
            final_output += f"Error: executing Python file: {e}"

        return final_output
    except Exception as e:
        return f'Error: {str(e)}\n'