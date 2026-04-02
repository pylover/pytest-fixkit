import os
import socket
import shutil
import tempfile
import contextlib
from unittest import mock

import pytest


__all__ = [
    'tmpdir',
    'mktmpdir',
    'mktmpfile',
    'mktmptree',
    'chdir',
    'redis',
    'freetcpport'
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


@pytest.fixture
def redis():

    class RedisMock:
        def __init__(self, **kw):
            self.info = kw
            self.maindict = dict()

        def srem(self, key, member):
            set_ = self.maindict.setdefault(key, set())
            if member in set_:
                set_.remove(member)

        def sadd(self, key, member):
            set_ = self.maindict.setdefault(key, set())
            set_.add(member)

        def sismember(self, key, member):
            return key in self.maindict and \
                member in self.maindict[key]

        def get(self, key):
            return self.maindict.get(key, '').encode()

        def set(self, key, value):
            self.maindict[key] = value

        def setnx(self, key: str, value):
            if not self.maindict.get(key):
                self.set(key, value)
                return 1
            return 0

        def hset(self, key, field, value):
            hashtable = self.maindict.setdefault(key, {})
            hashtable[field] = value

        def hget(self, key, field):

            hashtable = self.maindict.setdefault(key, {})
            return hashtable[field].encode()

        def flushdb(self):
            self.maindict.clear()

        def close(self):
            # Do nothing here, this methog is needed for just compatibiliy.
            pass

    with mock.patch('redis.Redis', new=RedisMock) as p:
        yield p


@pytest.fixture
def freetcpport():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(('localhost', 0))
        return s.getsockname()[1]
    finally:
        s.close()


# @pytest.fixture()
# def htmlfile():
#     @contextlib.contextmanager
#     def create(filename, title, cssfile=None):
#         with open(filename, 'a') as file:
#             file.truncate(0)
#             file.write(
#                 '<!DOCTYPE html>\n'
#                 '<html lang="en">\n'
#                 '<head>\n'
#                 '<meta charset="utf-8" />\n'
#                 f'<title>{title}</title>\n'
#             )
#
#             if cssfile:
#                 file.write(f'<link rel="stylesheet" href="{cssfile}" '
#                            'type="text/css" />\n')
#
#             file.write('</head><body>\n')
#             yield file
#             file.write('</body></html>')
#
#     return create
