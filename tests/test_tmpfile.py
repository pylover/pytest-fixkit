import os


def test_tmpfile(mktmpfile):
    filename = mktmpfile()
    assert os.path.exists(filename)

    filename = mktmpfile(name='foo.txt')
    assert os.path.exists(filename)
    assert os.path.basename(filename) == 'foo.txt'

    filename = mktmpfile(content='foo bar baz')
    with open(filename) as f:
        assert f.read() == 'foo bar baz'
