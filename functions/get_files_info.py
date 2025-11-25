import os
from google import genai
from google.genai import types
from functions.config import MAX_CHARS


# get files infor in a directory
def get_files_info(working_directory, directory="."):
    absolute_path_directory = os.path.abspath(os.path.join(working_directory, directory))
    absolute_path_working_directory = os.path.abspath(working_directory)

# check if directory in working directory
    if not absolute_path_directory.startswith(absolute_path_working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

# check if it is a directory    
    if not os.path.isdir(absolute_path_directory):
        return f'Error: "{directory}" is not a directory'
    
    else:
        try:
            list_content = os.listdir(absolute_path_directory)
            new_list = []

# get file size and check if it is a directory
            for item in list_content:
                item_path = os.path.join(absolute_path_directory, item)
                if os.path.isdir(item_path):
                    file_size = os.path.getsize(item_path)
                    new_list.append(f"- {item}: file_size={file_size} bytes, is_dir=True")
                                
                elif os.path.isfile(item_path):
                    file_size = os.path.getsize(item_path)
                    new_list.append(f"- {item}: file_size={file_size} bytes, is_dir=False")

# reformate files infor
            formatted_content = "\n".join(new_list)   

            return formatted_content
    
        except Exception as e:
            return f"Error: {e}"    


# build schema for get_files_infor   
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


# build schema for get_file_content
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads and returns the first {MAX_CHARS} characters of the content from a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file whose content should be read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)


# build schema for run_python_file
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)



#build schema for write_file
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file within the working directory. Creates the file if it doesn't exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
        required=["file_path", "content"],
    ),
)


# create a list of all the available functions
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)