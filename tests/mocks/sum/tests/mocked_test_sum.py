from tests.mocks.sum.src.mocked_sum import simple_sum
import pytest


def test_simple_sum():
    assert simple_sum(2, 2) == 4


@pytest.mark.xfail
def test_fail_simple_sum():
    assert simple_sum(2, 2) == 3
