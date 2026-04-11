import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from main import app
from src.services import quiz_service


@pytest.fixture(autouse=True)
def _reset_store():
    quiz_service.reset()
    yield
    quiz_service.reset()


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
