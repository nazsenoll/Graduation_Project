import os
import shutil

def delete_folder_if_exists(folder_path):
    """Delete the specified folder if it exists, along with all its contents."""
    try:
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
            print(f"{folder_path} has been deleted.")
        else:
            print(f"{folder_path} does not exist.")
    except Exception as e:
        print(f"Error: {e}")


def delete_file_if_exists(file_path):
    """Delete the specified file if it exists."""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"{file_path} has been deleted.")
        else:
            print(f"{file_path} does not exist.")
    except Exception as e:
        print(f"Error: {e}")


def create_file_if_not_exist(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    if not os.path.exists(file_path):
        with open(file_path, 'a+'):
            pass

def createDirectoriesIfNotExist(directories):
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
