import threading
from tdd_monitor.src.chore.trigger_test import trigger_test
from tdd_monitor.src.file_handling.compare_files import compare_files
from tdd_monitor.src.chore.signal_handler import EXIT_EVENT


def monitor(
    base_file: str, file_path: str, tests_path: str = None
):
    if EXIT_EVENT.is_set():
        return 0
    if tests_path is None:
        tests_path = file_path

    check = compare_files(base_file, file_path)
    if check is not False:
        base_file = check
        trigger_test(tests_path)

    recursively_call = threading.Timer(
        2,
        monitor,
        [
            base_file,
            file_path,
            tests_path
        ]
    )
    recursively_call.start()
