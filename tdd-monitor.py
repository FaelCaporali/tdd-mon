import sys
import os
import threading
import re
import signal
import time
import pytest

# TO-DOS:
#   configure exit signal properly
#   on creating file, write the boilerplate
#   create folders if not exists
#   accept entire folder for monitoring
#   lint-it
#   make-it-a-pip-package

# DREAMS:
#   entire monitoring cli/gui framework
#       1. provide root dir
#       2. scan for supported libs or
#           ask for lib of preference
#
#       3. scan for source codes or
#           ask for route dir of source codes to be tested
#
#       4. run available tests
#       5. start monitoring changes on tests files or source code files
#       6. run relevant tests if changes are noticed


EXIT_EVENT = threading.Event()
ARGS_ERROR = IndexError(
    "Invalid arguments!\nUsage:\npython3 test_fizz_buzz.py /path/to/tested/file.py"
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


def create_file(file_path: str):
    print(f"\n-----\nCreating file at {file_path}")
    create = open(file_path, mode="w")
    create.close()
    print("\nFile created! Happy testing!\n-----\n")


def treat_arguments(arguments: list[str]):
    if len(arguments) != 2:
        raise ARGS_ERROR

    file_name = get_file_name(arguments[1])

    if not os.path.isfile(arguments[1]):
        create_file(arguments[1])

    if not os.path.isfile(f"tests/tests_{file_name}"):
        create_file(f"tests/tests_{file_name}")


def have_file_changed(base_file: str, file_path: str) -> bool | str:
    with open(file_path) as raw_reader:
        newer_version = raw_reader.read()
        if newer_version != base_file:
            return newer_version
    return False


def do_the_test(file_path: str, file_type: str):
    print("\n-----")
    print("New test starting...")
    print("-----\n")
    time.sleep(0.5)
    test_path = ""

    if file_type == "code":
        test_path = f"tests/tests_{get_file_name(file_path)}"
    else:
        test_path = file_path
    # must clean inside pytest process chache -> used pytest-xdist
    pytest.main([test_path, "--cache-clear", "--no-header", "-v", "-n", "auto"])


def main(base_file: str, file_path: str, file_type):
    if EXIT_EVENT.is_set():
        return 0

    check = have_file_changed(base_file, file_path)

    if check is not False:
        base_file = check
        do_the_test(file_path, file_type)

    recursively_call = threading.Timer(2, main, [base_file, file_path, file_type])
    recursively_call.start()


if __name__ == "__main__":
    """ "
    Monitor a file, and run automate tests on it if changes are noticed.
    Made for TDD implementation.

    -----

    USAGE:
        python3 -m test-monitor (/path/to/file/to/be/tested)

    -----
    """
    try:
        print("-----\n")
        print("Welcome to TDD unit test monitor")
        print("\n-----")
        time.sleep(1.2)
        # TREAT CLI ARGUMENTS
        arguments = sys.argv
        treat_arguments(arguments)

        # SET UP SIGNAL HANDLER TO GRACEFULLY EXIT
        signal.signal(signal.SIGINT, exit_handler)

        # MAKE A FIRST READING OF THE FILES
        file_path = arguments[1]
        test_path = f"tests/tests_{get_file_name(file_path)}"
        first_sc_read: str = ""
        first_tsc_read: str = ""
        with open(file_path, mode="r") as source_code:
            first_sc_read = source_code.read()
        with open(test_path, mode="r") as test_source_code:
            first_tsc_read = test_source_code.read()

        # RUN A INITIAL TEST
        print("Running first test...\n")
        time.sleep(1)
        do_the_test(file_path, "code")

        print("\n\nMonitor is on, at any change, the test will run again")
        print("To leave use classic ctrl+c\n")

        # LOOP INFINITELY LOOKING UP FOR CHANGES
        main(first_sc_read, file_path, "code")
        main(first_tsc_read, test_path, "test")

    except IndexError:
        raise IndexError
    except FileNotFoundError:
        print("Não foi encontrado o caminho.")
        print("tdd-u.monitor somente cria arquivos")
        print("Tem certeza que os diretórios existem nos locais especificados?")
        raise FileNotFoundError
    except AssertionError:
        print(f"O teste falhou: {AssertionError}")
    except KeyboardInterrupt:
        sys.exit(0)
