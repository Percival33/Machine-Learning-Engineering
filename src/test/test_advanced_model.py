from src.models.advanced_model import AdvancedModel
from src.test.mocks import (
    tracks_sample,
    tracks_sample_sorted,
    genres_with_stats_sample,
    playlists_sample,
)


def test_sort_tracks():
    assert AdvancedModel.sort_tracks(tracks_sample()) == tracks_sample_sorted()


def test_validate_data():
    AdvancedModel.validate_data(genres_with_stats_sample())


def test_get_most_popular_groups_low_popularity():
    groups = {0, 1}
    assert AdvancedModel.get_most_popular_groups(30, tracks_sample_sorted()) == groups


def test_get_most_popular_groups_medium_popularity():
    groups = {0}
    assert AdvancedModel.get_most_popular_groups(59, tracks_sample_sorted()) == groups


def test_get_most_popular_groups_high_popularity():
    groups = set()
    assert AdvancedModel.get_most_popular_groups(90, tracks_sample_sorted()) == groups


def test_make_playlists():
    model = AdvancedModel(track_limit_per_playlist=5)
    assert model.make_playlists(tracks_sample_sorted(), {0, 1}) == playlists_sample()
