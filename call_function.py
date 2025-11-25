from google.genai import types

from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python import run_python_file, schema_run_python_file
from functions.write_file_content import write_file, schema_write_file
from config import WORKING_DIR

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)


# Create a new function that will handle the abstract task of calling one of our four functions
def call_function(function_call_part, verbose=False):
# If verbose is specified, print the function name and args:
    if verbose:
        print(
            f" - Calling function: {function_call_part.name}({function_call_part.args})"
        )
# Otherwise, just print the name
    else:
        print(f" - Calling function: {function_call_part.name}")

# call the function and capture the result
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }
    function_name = function_call_part.name

# If the function name is invalid, return a types.Content that explains the error
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
# manually add the "working_directory" argument to the dictionary of keyword arguments
    args = dict(function_call_part.args)
    args["working_directory"] = WORKING_DIR
    function_result = function_map[function_name](**args)
# Return types.Content with a from_function_response describing the result of the function call
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
