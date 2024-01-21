from fastapi.testclient import TestClient

from service import app, run_model_dependency, run_model_for_user
import mocks

client = TestClient(app)

app.dependency_overrides[run_model_dependency] = mocks.run_model
app.dependency_overrides[run_model_for_user] = mocks.run_model_for_user


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
    with fastapi_dep(app).override({run_model_dependency: mocks.run_model_error}):
        response = client.get("/predict/model/base")
        assert response.status_code == 404


def test_playlist_success():
    response = client.get("/playlists/123")
    assert response.status_code == 200
    assert response.json() == {"playlists": ["data"]}
