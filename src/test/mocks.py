from fastapi import HTTPException
import pandas as pd
from pandas import DataFrame
import os
from src.domain.Track import Track
from src.domain.Playlist import Playlist

TRACKS_SAMPLE_PATH = "file://" + os.path.abspath(
    os.path.join(
        __file__, "..", "..", "..", "data", "test", "tracks_sample.jsonl"
    )
)

STATS_SAMPLE_PATH = "file://" + os.path.abspath(
    os.path.join(
        __file__, "..", "..", "..", "data", "test", "genres_with_stats_sample.jsonl"
    )
)

POPULARITY_SAMPLE_PATH = "file://" + os.path.abspath(
    os.path.join(
        __file__, "..", "..", "..", "data", "test", "genres_with_popularity_sample.jsonl"
    )
)


async def run_model(model_type: str):
    class OutputMock:
        stdout = '{"some": "data"}'

    mock = OutputMock()
    print(mock.stdout)
    return mock


async def run_model_for_user(user_id: int):
    class OutputMock:
        stdout = '["data"]'

    mock = OutputMock()
    print(mock.stdout)
    return mock


async def run_model_error():
    raise HTTPException(status_code=404, detail="File Not Found")


def genres_with_stats_sample() -> DataFrame:
    stats_data = pd.read_json(STATS_SAMPLE_PATH, lines=True)
    corrected_data = stats_data.drop(columns=["track_id", "genre"]).drop_duplicates(
        keep="first"
    )
    return corrected_data


def tracks_sample() -> list[Track]:
    tracks_data = pd.read_json(TRACKS_SAMPLE_PATH, lines=True)
    tracks = list()
    for index, row in tracks_data.iterrows():
        tracks.append(Track(row["id"], row["popularity"], int(index) % 2))
    return tracks


def genres_with_popularity_sample() -> DataFrame:
    popularity_data = pd.read_json(POPULARITY_SAMPLE_PATH, lines=True)
    return popularity_data


def tracks_sample_sorted() -> dict[int, list[Track]]:
    sorted_tracks = dict()
    tracks_first_group = [
        Track("0RNxWy0PC3AyH4ThH3aGK6", 61, 0),
        Track("4Pnzw1nLOpDNV6MKI5ueIR", 62, 0),
        Track("6kD1SNGPkfX9LwaGd1FG92", 63, 0),
        Track("5DIVWgTeJ2fPIxaY9e7ZKn", 64, 0),
        Track("0Hsc0sIaxOxXBZbT3ms2oj", 65, 0),
    ]
    tracks_second_group = [
        Track("2W889aLIKxULEefrleFBFI", 51, 1),
        Track("7GLmfKOe5BfOXk7334DoKt", 52, 1),
        Track("5RcvlmVx2xtFcp2Ta5pw7X", 53, 1),
        Track("0x0ffSAP6PkdoDgHOfroof", 54, 1),
        Track("3aEJMh1cXKEjgh52claxQp", 55, 1),
    ]
    sorted_tracks[0] = tracks_first_group
    sorted_tracks[1] = tracks_second_group

    return sorted_tracks


def playlists_sample() -> list[Playlist]:
    playlists = list()
    sorted_tracks = tracks_sample_sorted()

    for group, tracks in sorted_tracks.items():
        new_playlist = Playlist()
        for track in tracks:
            new_playlist.add(track)
        playlists.append(new_playlist)

    return playlists


def genre_playlist(sort: bool) -> dict[str, Playlist]:
    genres = dict()
    tracks = [
        Track("823asFDfgdfgDGDHjKKeet", 60, -1),
        Track("17gxfuiFUrLhbUKdunxUPJ", 58, -1),
        Track("0RNxWy0PC3AyH4ThH3aGK6", 55, -1),
    ]
    jazz_playlist = Playlist(max_size=5)
    rock_playlist = Playlist(max_size=5)
    pop_playlist = Playlist(max_size=5)

    jazz_playlist.add(tracks[0])

    if sort:
        rock_playlist.add(tracks[1])
        rock_playlist.add(tracks[2])

        pop_playlist.add(tracks[1])
        pop_playlist.add(tracks[2])
    else:
        rock_playlist.add(tracks[2])
        rock_playlist.add(tracks[1])

        pop_playlist.add(tracks[2])
        pop_playlist.add(tracks[1])

    genres["jazz"] = jazz_playlist
    genres["rock"] = rock_playlist
    genres["pop"] = pop_playlist

    return genres