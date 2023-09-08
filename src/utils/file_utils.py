import os

def get_path(file, relative_path):
    current_file_path = os.path.abspath(file)
    current_directory = os.path.dirname(current_file_path)
    
    return os.path.join(current_directory, relative_path)