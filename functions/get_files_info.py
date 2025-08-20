# Function to get information about files in a directory

import os


def get_files_info(working_directory, directory="."):
    full_path = os.path.abspath(os.path.join(working_directory, directory))

    # Validate that the full path is not outside the working directory
    if not full_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory\n'
    
    # Check to make sure the full path is a directory
    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory\n'
    
    try:
        files = os.listdir(full_path)
        output = ""
        for file in files:
            output += f" - {file}: file_size={os.path.getsize(os.path.join(full_path, file))} bytes, is_dir={os.path.isdir(os.path.join(full_path, file))}\n"
        return output
    except Exception as e:
        return f'Error: {str(e)}\n'
    