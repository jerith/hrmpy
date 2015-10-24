import pytest


class CachedSys(object):
    def __init__(self, capsys):
        self.capsys = capsys
        self._out = ""
        self._err = ""

    def _update(self):
        out, err = self.capsys.readouterr()
        self._out += out
        self._err += err

    @property
    def out(self):
        self._update()
        return self._out

    @property
    def err(self):
        self._update()
        return self._err

    @property
    def output_data(self):
        return " ".join(self.out.split())


@pytest.fixture
def cachedsys(capsys):
    return CachedSys(capsys)
