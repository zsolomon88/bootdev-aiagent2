import os

MAX_FILE_SIZE = 10000  # Maximum file size to read in bytes

def get_file_content(working_directory, file_path):
    full_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Validate that the full path is not outside the working directory
    if not full_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory\n'
    
    # Check to make sure the full path is a file
    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}\n"'
    
    try:
        file_size = os.path.getsize(full_path)
        with open(full_path, 'r', encoding='utf-8') as file:
            content = file.read(MAX_FILE_SIZE)
            if file_size > MAX_FILE_SIZE:
                content += f'[...File "{file_path}" truncated at {MAX_FILE_SIZE} characters]'
        return content
    except Exception as e:
        return f'Error: {str(e)}\n'