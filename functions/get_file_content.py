import os
from functions.config import *


# get contents of a file
def get_file_content(working_directory, file_path):
    absolute_path_file = os.path.abspath(os.path.join(working_directory, file_path))
    absolute_path_working_directory = os.path.abspath(working_directory)

# check if file path is outside working directory
    if not absolute_path_file.startswith(absolute_path_working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
# check if file path is a file
    if not os.path.isfile(absolute_path_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(absolute_path_file, "r") as f:
            file_content = f.read()

# check length of file
            if len(file_content) > MAX_CHARS:
                message = f'...File "{file_path}" truncated at {MAX_CHARS} characters'
                file_content_string = file_content[:MAX_CHARS] 
                result = file_content_string + message
                return result
            
            else:
                return file_content
  
    except Exception as e:
        return f"Error: {e}"    

    
