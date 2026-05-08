def test_fileio(fileio):
    file = fileio('foo bar baz', 'foo.txt')
    assert 'foo bar baz' == file.read()

    file = fileio(b'foo bar baz', 'foo.img')
    assert b'foo bar baz' == file.read()
