import os
from tdd_monitor.src.errors.args_error import ARGS_ERROR
from tdd_monitor.src.file_handling.create_file import create_file
from tdd_monitor.src.file_handling.get_file_name import get_file_name


def parser(arguments: list[str]):
    try:
        if len(arguments) < 2:
            raise ARGS_ERROR
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

        return "tests/", f"test_{file_name}"

    elif len(arguments) == 3:
        test_file_path = arguments[2]
        tf_ending = test_file_path[-3:]

        if tf_ending == ".py":
            if not os.path.isfile(test_file_path):
                create_file(test_file_path)
            return "tests/", get_file_name(test_file_path)
        else:
            return arguments[2], False

    else:
        raise ARGS_ERROR
