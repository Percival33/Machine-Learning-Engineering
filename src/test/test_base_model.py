from src.models.base_model import BaseModel
from src.test.mocks import genres_with_popularity_sample, genre_playlist


def test_base_model_predict():
    model = BaseModel(track_limit_per_playlist=5)
    assert model.predict(genres_with_popularity_sample()) == genre_playlist(sort=True)


def test_base_model_make_playlists():
    model = BaseModel(track_limit_per_playlist=5)
    assert model.create_playlists(genres_with_popularity_sample()) == genre_playlist(sort=False)
