import json
import sys
from collections import defaultdict
from typing import Any

import pandas as pd
import os

from pandas import DataFrame

from src.domain.Playlist import Playlist
from src.domain.Track import Track
from src.models.ABCSolver import AbstractSolver

DATA_PATH = "file://" + os.path.abspath(
    os.path.join(
        __file__, "..", "..", "..", "data", "processed", "exploded_genres_with_popularity.jsonl"
    )
)


class BaseModel(AbstractSolver):
    def __init__(self, songs_in_genre=500, track_limit_per_playlist=10, number_of_playlists=5):
        """
        Initialize BaseModel with parameters.
        Default parameters: {'songs_in_genre': 500, 'playlist_limit': 10, 'number_of_playlists': 5}.
        """
        self.parameters = {
            "songs_in_genre": songs_in_genre,
            "track_limit_per_playlist": track_limit_per_playlist,
            "number_of_playlists": number_of_playlists,
        }

    def fit(self, X, y) -> None:
        pass

    def get_parameters(self) -> dict[str, int]:
        return self.parameters

    @staticmethod
    def validate_data(X: DataFrame) -> None:
        required_columns = {"track_id", "genre", "popularity"}
        if not required_columns.issubset(X.columns):
            raise ValueError(f"Data must contain columns: {required_columns}")

    def create_playlists(self, X: DataFrame) -> defaultdict[Any, Playlist]:
        track_limit = self.parameters["track_limit_per_playlist"]
        genres = defaultdict(lambda: Playlist(track_limit))
        for _, row in X.iterrows():
            track_id, genre, popularity = row
            genres[genre].add(Track(track_id, popularity, -1))
        return genres

    def predict(self, X: DataFrame) -> dict[str, list[Playlist]]:
        self.validate_data(X)
        X = X.sort_values(by="popularity", ascending=False)
        genres = self.create_playlists(X)

        sorted_playlists = sorted(genres.items(), key=lambda x: x[1].mean, reverse=True)
        top_playlists = sorted_playlists[: self.parameters["number_of_playlists"]]
        return {genre: playlist for genre, playlist in top_playlists}


if __name__ == "__main__":
    try:
        data = pd.read_json(DATA_PATH, lines=True)
        track_limit = 10
        if len(sys.argv) > 1:
            try:
                track_limit = int(sys.argv[1])
            except ValueError:
                print("Warning: Invalid track limit provided. Using default value of 10.")

        model = BaseModel(track_limit_per_playlist=track_limit)
        res = model.predict(data)
        unique_songs = set()

        response = []
        for genre, playlist in res.items():
            response.append(
                {
                    "size": playlist.size,
                    "min_track_popularity": playlist.min,
                    "max_track_popularity": playlist.max,
                    "mean_popularity": f"{playlist.mean:.2f}",
                    "tracks": [track.to_json_serializable() for track in playlist.tracks],
                }
            )

        print(json.dumps(response))
    except Exception as e:
        print(f"An error occurred: {e}")
