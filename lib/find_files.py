import os

import os


def find_files(directory, filter):
    # Get all files under the directory
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_list.append(file_path)

    files = [item for item in file_list if filter in item]
    return files
