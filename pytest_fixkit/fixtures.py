import os
import shutil
import tempfile
import contextlib

import pytest


__all__ = [
    'tmpdir',
    'mktmpdir',
    'mktmpfile',
    'mktmptree',
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
def mktmpdir():
    dirs = []

    def make():
        tdir = tempfile.mkdtemp()
        dirs.append(tdir)
        return tdir

    yield make
    for d in dirs:
        shutil.rmtree(d)


@pytest.fixture
def mktmpfile(mktmpdir):
    files = []
    def make(name=None, content=None):
        if not name:
            name = tempfile.mktemp()

        name = os.path.join(mktmpdir(), name)
        with open(name, 'w') as f:
            if content:
                f.write(content)

        files.append(name)
        return os.path.abspath(name)

    yield make
    for f in files:
        os.remove(f)


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


@pytest.fixture
def mktmptree():
    temp_directories = []

    def create_nodes(root, tree):
        for k, v in tree.items():
            name = os.path.join(root, k)

            if isinstance(v, dict):
                os.mkdir(name)
                create_nodes(name, v)
                continue

            if hasattr(v, 'read'):
                f = v
                v = f.read()
                f.close()

            mode = 'w'
            if isinstance(v, bytes):
                mode += 'b'

            with open(name, mode) as f:
                f.write(v)

    def _make_temp_directory(tree):
        """Structure example: {'a.html': 'Hello', 'b': {}}."""
        root = tempfile.mkdtemp()
        temp_directories.append(root)
        create_nodes(root, tree)
        return root

    yield _make_temp_directory

    for d in temp_directories:
        shutil.rmtree(d)
