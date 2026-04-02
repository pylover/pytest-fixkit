import os


def test_tmpfile(tmpfile):
    with tmpfile() as filename:
        assert os.path.exists(filename)

    with tmpfile(name='foo.txt') as filename:
        assert os.path.exists(filename)
        assert os.path.basename(filename) == 'foo.txt'

    with tmpfile(content='foo bar baz') as filename:
        with open(filename) as f:
            assert f.read() == 'foo bar baz'
