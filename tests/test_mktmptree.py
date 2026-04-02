import os
import io


def test_mktmptree(mktmptree):
    textfile = io.StringIO('Baz Lorem ipsum')
    binfile = io.BytesIO(b'Qux Lorem ipsum')
    tree = mktmptree({
        'foo': {
            'foo.txt': 'Lorem ipsum',
            'foo.md': '# Lorem ipsum',
        },
        'bar': {},
        'baz': textfile,
        'qux.bin': binfile,
    })

    assert os.path.isfile(f'{tree}/foo/foo.txt')
    assert os.path.isfile(f'{tree}/foo/foo.md')
    assert os.path.isdir(f'{tree}/bar')
    assert os.path.isfile(f'{tree}/baz')
    with open(f'{tree}/baz') as f:
        assert f.read() == 'Baz Lorem ipsum'

    with open(f'{tree}/qux.bin', 'rb') as f:
        assert f.read() == b'Qux Lorem ipsum'
