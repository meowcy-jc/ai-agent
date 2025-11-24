import os


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
            for file in list_content:
                item_path = os.path.join(absolute_path_directory, file)
                if os.path.isdir(item_path):
                    file_size = os.path.getsize(item_path)
                    new_list.append(f"- {file}: file_size={file_size} bytes, is_dir=True")
                                
                elif os.path.isfile(item_path):
                    file_size = os.path.getsize(item_path)
                    new_list.append(f"- {file}: file_size={file_size} bytes, is_dir=False")

# reforamte files infor
            formatted_content = "\n".join(new_list)   

            return formatted_content
    
        except Exception as e:
            return f"Error: {e}"    

        