import pytest

from supriya.nonrealtime import Session
from supriya.realtime import Server
from supriya.assets.synthdefs import default


@pytest.fixture
def server():
    server = Server()
    server.boot()
    default.allocate(server=server)
    yield server
    server.quit()


@pytest.fixture
def session():
    yield Session()
