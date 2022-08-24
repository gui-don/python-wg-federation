""" hello.py test suit """
from wg_federation.hello import Hello


class TestHello:
    """ Test Hello class """

    def test_hello(self, capsys):
        """ Test: hello """
        _hello: Hello = Hello()
        _hello.hello('3')

        captured = capsys.readouterr()
        assert captured.out == 'Hello! from version 3\n'
