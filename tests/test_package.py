from pytest_fixkit import *


def test_package():
    assert tmpdir
    assert tmpfile
    assert chdir
