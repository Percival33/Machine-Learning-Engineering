from collections import defaultdict

import pandas as pd
import os

from src.domain.Playlist import Playlist
from src.domain.Track import Track
from src.models.ABCSolver import AbstractSolver

DATA_PATH = os.path.abspath(
    os.path.join(".", "..", "..", "data", "processed", "exploded_genres_with_popularity.jsonl")
)


class BaseModel(AbstractSolver):
    def __init__(self, parameters=None):
        """
        Initialize BaseModel with parameters.
        Default parameters: {'songs_in_genre': 500, 'playlist_limit': 20}.
        """
        self.parameters = (
            parameters
            if parameters
            else {"songs_in_genre": 500, "track_limit_per_playlist": 20, "number_of_playlists": 5}
        )

    def fit(self, X, y) -> None:
        pass

    def get_parameters(self):
        return self.parameters

    @staticmethod
    def validate_data(X):
        required_columns = {"track_id", "genre", "popularity"}
        if not required_columns.issubset(X.columns):
            raise ValueError(f"Data must contain columns: {required_columns}")

    def create_playlists(self, X):
        track_limit = self.parameters["track_limit_per_playlist"]
        genres = defaultdict(lambda: Playlist(track_limit))
        for _, row in X.iterrows():
            track_id, genre, popularity = row
            genres[genre].add(Track(track_id, popularity))
        return genres

    def predict(self, X):
        self.validate_data(X)
        X = X.sort_values(by="popularity", ascending=False)
        genres = self.create_playlists(X)

        sorted_playlists = sorted(genres.items(), key=lambda x: x[1].mean, reverse=True)
        top_playlists = sorted_playlists[: self.parameters["number_of_playlists"]]
        return {genre: playlist for genre, playlist in top_playlists}


if __name__ == "__main__":
    data = pd.read_json(DATA_PATH, lines=True)
    model = BaseModel()
    res = model.predict(data)
    unique_songs = set()

    for genre, playlist in res.items():
        print(f"Genre: {genre}")
        print(f"  Size: {playlist.size}")
        print(f"  Sum: {playlist.sum}")
        print(f"  Min Popularity: {playlist.min}")
        print(f"  Max Popularity: {playlist.max}")
        print(f"  Mean Popularity: {playlist.mean:.2f}")
        # print(f"  Playlist: {playlist}")
        print("-" * 30)

        for track in playlist.tracks:
            unique_songs.add(track)

    print(len(unique_songs))
