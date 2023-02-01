import re


def get_file_name(file_path: str):
    splitted_path = re.split("/", file_path)
    return splitted_path[len(splitted_path) - 1]
