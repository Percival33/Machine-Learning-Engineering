from fastapi import HTTPException
from fastapi.testclient import TestClient

from service import app, run_model_dependency, run_model_for_user

client = TestClient(app)


async def override_dependency(model_type: str):
    class OutputMock:
        stdout = '{"some": "data"}'

    mock = OutputMock()
    print(mock.stdout)
    return mock


async def override_dependency_2(user_id: int):
    class OutputMock:
        stdout = '["data"]'

    mock = OutputMock()
    print(mock.stdout)
    return mock


async def override_dependency_failure():
    raise HTTPException(status_code=404, detail="File Not Found")


app.dependency_overrides[run_model_dependency] = override_dependency
app.dependency_overrides[run_model_for_user] = override_dependency_2


def test_index_redirects_to_docs():
    response = client.get("/")
    assert response.status_code == 200
    assert str(response.url).endswith("/docs")


def test_predict_model_success():
    response = client.get("/predict/model/base")
    print(response)
    assert response.status_code == 200
    assert response.json() == {"model_type": "base", "playlists": {"some": "data"}}


def test_predict_model_failure(fastapi_dep):
    with fastapi_dep(app).override({run_model_dependency: override_dependency_failure}):
        response = client.get("/predict/model/base")
        print(response.headers, response.url, response.json())

        assert response.status_code == 404


def test_playlist_success():
    response = client.get("/playlists/123")
    assert response.status_code == 200
    assert response.json() == {"playlists": ["data"]}
