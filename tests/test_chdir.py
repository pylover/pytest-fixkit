import os


def test_chdir(chdir, tmpdir):
    here = os.getcwd()

    with chdir(tmpdir):
        assert os.path.samefile(os.getcwd(), tmpdir)

    assert os.path.samefile(os.getcwd(), here)
