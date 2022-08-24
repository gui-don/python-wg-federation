""" hello.py test suit """
import re
from wg_federation import main


class TestMain:
    """ Test main """

    def test_main(self, capsys):
        """ Test: main """
        main()

        captured = capsys.readouterr()
        assert re.findall(r'Hello!.*', captured.out)
