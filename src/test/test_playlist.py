import pytest
from src.domain.Track import Track
from src.domain.Playlist import Playlist


def create_track(track_id, popularity, group):
    return Track(track_id=track_id, popularity=popularity, group=group)


def test_playlist_initialization():
    playlist = Playlist(max_size=10)
    assert playlist.size == 0
    assert playlist.sum == 0
    assert playlist.min == float("inf")
    assert playlist.max == float("-inf")
    assert playlist.mean == 0.0
    assert playlist.MAX_SIZE == 10


def test_add_track_to_playlist():
    playlist = Playlist(max_size=10)
    track = create_track("track1", 50, 1)
    playlist.add(track)
    assert playlist.size == 1
    assert playlist.sum == 50
    assert playlist.min == 50
    assert playlist.max == 50
    assert playlist.mean == 50


def test_playlist_limit():
    playlist = Playlist(max_size=2)
    track1 = create_track("track1", 70, 1)
    track2 = create_track("track2", 30, 1)
    track3 = create_track("track3", 50, 1)
    playlist.add(track1)
    playlist.add(track2)
    playlist.add(track3)

    assert playlist.size == 2
    # as track2 has the lowest popularity
    assert track2 not in playlist.tracks
    assert track1 in playlist.tracks
    assert track3 in playlist.tracks
    assert playlist.min == 50
    assert playlist.max == 70
    assert playlist.mean == 60


def test_playlist_limit_with_empty_playlist():
    playlist = Playlist(max_size=2)
    playlist.limit()  # Calling limit on an empty playlist
    assert playlist.size == 0
    assert playlist.min == float("inf")
    assert playlist.max == float("-inf")
    assert playlist.mean == 0
