

def test_redis(redis):
    r = redis()

    # set/get
    r.set('foo', 'FOO')
    assert r.get('foo') == b'FOO'

    # sadd/srem
    r.sadd('bar', 'BAR')
    assert r.sismember('bar', 'BAR')
    r.srem('bar', 'BAR')
    assert not r.sismember('bar', 'BAR')

    # setnx
    r.setnx('baz', 'BAZ')
    assert r.get('baz') == b'BAZ'
    r.setnx('baz', 'ZAB')
    assert r.get('baz') == b'BAZ'

    # hset/hget
    r.hset('quux', 'foo', 'FOO')
    assert r.hget('quux', 'foo') == b'FOO'

    r.flushdb()
    assert r.get('foo') == b''

    r.close()
