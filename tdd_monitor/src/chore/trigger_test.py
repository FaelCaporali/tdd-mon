from tdd_monitor.src.templates.init_test import init_log
import pytest


def trigger_test(test_path: str):
    init_log(test_path)
    pytest.main([test_path, "--cache-clear", "-vv", "-n", "auto"])
