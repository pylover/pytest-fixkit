import os
import shutil
import tempfile
import contextlib

import pytest


__all__ = [
    'tmpdir',
    'tmpfile',
    'chdir',
]


@pytest.fixture
def tmpdir():
    tdir = tempfile.mkdtemp()
    try:
        yield tdir
    finally:
        shutil.rmtree(tdir)


@pytest.fixture
def tmpfile(tmpdir):
    @contextlib.contextmanager
    def make(name=None, content=None):
        if not name:
            name = tempfile.mktemp()

        name = os.path.join(tmpdir, name)
        with open(name, 'w') as f:
            if content:
                f.write(content)

        try:
            yield os.path.abspath(name)
        finally:
            os.remove(name)

    return make


@pytest.fixture
def chdir():
    @contextlib.contextmanager
    def change(d):
        backup = os.getcwd()
        os.chdir(d)
        try:
            yield
        finally:
            os.chdir(backup)

    return change
