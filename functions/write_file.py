import os


# give agent ability to write and overwrite files
def write_file(working_directory, file_path, content):
    absolute_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    absolute_working_directory_path = os.path.abspath(working_directory)

    # check if file path is outside working directory
    if not absolute_file_path.startswith(absolute_working_directory_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    # if file doesn't exist, create one
    try:
        dir_path = os.path.dirname(absolute_file_path)
        if dir_path and not os.path.exists(dir_path):
    # create directory
            os.makedirs(dir_path)
        
        with open(absolute_file_path, "w") as f:
            f.write(content)
        
    except Exception as e:
        return f"Error: {e}"

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'