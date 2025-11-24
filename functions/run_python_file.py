import os
import subprocess


def run_python_file(working_directory, file_path, args=[]):
    absolute_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    absolute_working_directory_path = os.path.abspath(working_directory)

    # check if file path is outside working directory
    if not absolute_file_path.startswith(absolute_working_directory_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    # check if file exists
    if not os.path.exists(absolute_file_path):
        return f'Error: File "{file_path}" not found.'
    
    #if file doesn't end with ".py"
    if not absolute_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    # execute file
    try:
        command = ["python3", absolute_file_path] + args
        complete_process = subprocess.run(command, capture_output=True, cwd=absolute_working_directory_path, timeout=30)
        stdout = complete_process.stdout.decode()
        stderr = complete_process.stderr.decode()
        result = ""
        if stdout != "":
            result += f"STDOUT:{stdout}"
        if stderr != "":
            result += f"STDERR:{stderr}"
        if complete_process.returncode != 0:
            return_code = complete_process.returncode
            result += f"Process exited with code {return_code}"

        if result == "":
            return "No output produced."
        
        return result
    
    except Exception as e:
        return f"Error: executing Python file: {e}"
