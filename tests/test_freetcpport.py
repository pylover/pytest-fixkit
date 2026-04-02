def test_freetcpport(freetcpport):
    assert 1024 < freetcpport <= 65535
