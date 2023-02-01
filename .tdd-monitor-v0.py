import sys
import os
import threading
import re
import signal
import time
import pytest
# import optparse


EXIT_EVENT = threading.Event()
ARGS_ERROR = IndexError(
    "Invalid arguments!\nUsage:\npython3 tdd-monitor.py /path/to/tested/file.py  /path/to/test/file"
)


def exit_handler(signal_number, frame):
    if signal_number == 2:
        print("\n-----\n")
        print("Exiting... Thanks for using!")
        print("\n-----")
    EXIT_EVENT.set()


def get_file_name(file_path: str):
    splitted_path = re.split("/", file_path)
    return splitted_path[len(splitted_path) - 1]


def read_tests(dir_path: str, test_file: str | bool) -> list[dict]:
    readings: list[dict] = []
    if test_file is False:
        files = os.listdir(dir_path)
        docs: list[str] = []
        for file in files:
            if file[-3:] == '.py' and file[:4] == 'test':
                docs.append(file)
        for file in docs:
            readings.append({
                'file': file,
                'content': read_file(f"{dir_path}/{file}")
            })
    else:
        readings.append({
            'file': test_file,
            'content': read_file(f"{dir_path}/{test_file}")
        })
    return readings


def read_file(file_path: str) -> str:
    with open(file_path, mode="r") as reader:
        return reader.read()


def create_file(file_path: str):
    print(f"\n-----\nCreating file at {file_path}")
    create = open(file_path, mode="w")
    create.close()
    print("\nFile created! Happy testing!\n-----\n")


def parse_arguments(arguments: list[str]):
    try:
        if arguments[1][-3:] != ".py":
            raise ARGS_ERROR
    except TypeError:
        raise ARGS_ERROR

    if not os.path.isfile(arguments[1]):
        create_file(arguments[1])
    file_name = get_file_name(arguments[1])

    if len(arguments) == 2:
        complete_test_path = f"tests/test_{file_name}"

        if not os.path.isfile(complete_test_path):
            create_file(complete_test_path)

        return file_name, 'tests/', f"test_{file_name}"

    elif len(arguments) == 3:
        test_file_path = arguments[2]
        tf_ending = test_file_path[-3:]

        if tf_ending == ".py":
            if not os.path.isfile(test_file_path):
                create_file(test_file_path)
            return file_name, 'tests', get_file_name(test_file_path)
        else:
            return file_name, arguments[2], False

    else:
        raise ARGS_ERROR


def have_file_changed(base_file: str, file_path: str) -> bool | str:
    with open(file_path) as raw_reader:
        newer_version = raw_reader.read()
        if newer_version != base_file:
            return newer_version
    return False


def do_the_test(file_path: str):
    print("\n-----")
    print("New test starting...")
    print("-----\n")
    #     test_path = file_path
    # must clean inside pytest process chache -> used pytest-xdist
    pytest.main(
        [file_path, "-n", "auto"]
    )


def monitor(base_file: str, file_path: str):
    if EXIT_EVENT.is_set():
        return 0

    check = have_file_changed(base_file, file_path)

    if check is not False:
        base_file = check
        do_the_test(file_path)

    recursively_call = threading.Timer(
        2, monitor, [base_file, file_path]
    )
    recursively_call.start()


if __name__ == "__main__":
    """ "
    Monitor a file, and run automate tests on it if changes are noticed.
    Made for TDD implementation.

    -----

    USAGE:
        python3 tdd-pymon (/path/to/file/to/be/tested) [optional/path/to/tests/folder/or/file]

    -----
    At any changes (source code or tests), the tests will be triggered
    """
    try:
        print("-----")
        print("Welcome to TDD unit test monitor")
        print("-----")

        # TREAT CLI ARGUMENTS
        arguments = sys.argv
        sc_path = arguments[1]
        sc_file, tests_dir, test_file = parse_arguments(arguments)

        # SET UP SIGNAL HANDLER TO GRACEFULLY EXIT
        signal.signal(signal.SIGINT, exit_handler)

        # MAKE A FIRST READING OF THE FILES
        first_sc_read: str = read_file(sc_path)
        first_tsc_read: list[str] = read_tests(tests_dir, test_file)

        print("\n\nMonitor is on, at any change, the test will run again")
        print("To leave use classic ctrl+c\n")

        #make a fist test
        for test in first_tsc_read:
            do_the_test(f"{tests_dir}/{test['file']}")

        # LOOP INFINITELY LOOKING UP FOR CHANGES
        monitor(first_sc_read, arguments[1], True)

        if test_file is None:
            for reading in first_tsc_read:
                monitor(reading["content"], f"{tests_dir}/{reading['file']}")
        else:
            monitor(first_tsc_read[0], f"{tests_dir}/{test_file}")

    except IndexError:
        raise IndexError
    except FileNotFoundError:
        print("Não foi encontrado o caminho.")
        print("tdd-u.monitor somente cria arquivos")
        print(
            "Tem certeza que os diretórios existem nos locais especificados?"
        )
        raise FileNotFoundError
    except AssertionError:
        print(f"O teste falhou: {AssertionError}")
    except KeyboardInterrupt:
        sys.exit(0)
