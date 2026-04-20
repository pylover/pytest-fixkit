def test_fileio(fileio):
    file = fileio('foo.txt', 'foo bar baz')
    assert 'foo bar baz' == file.read()

    file = fileio('foo.img', b'foo bar baz')
    assert b'foo bar baz' == file.read()
