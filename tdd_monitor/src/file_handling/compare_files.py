from tdd_monitor.src.file_handling.read_doc import read_doc


def compare_files(base_file: str, file_path: str) -> str | bool:
    newer_file = read_doc(file_path)
    if base_file != newer_file:
        return newer_file
    return False
