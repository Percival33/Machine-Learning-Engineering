import random
from collections import defaultdict

import pandas as pd
from random import sample
import os
from sklearn.cluster import KMeans

from src.domain.Playlist import Playlist
from src.domain.Track import Track
from src.models.ABCSolver import AbstractSolver

STATS_PATH = os.path.abspath(
    os.path.join(".", "..", "..", "data", "processed", "exploded_genres_with_stats.jsonl")
)

TRACKS_PATH = os.path.abspath(
    os.path.join(".", "..", "..", "data", "processed", "tracks_no_duplicates.jsonl")
)


class AdvancedModel(AbstractSolver):
    def __init__(self, parameters=None):
        """
        Initialize AdvancedModel with parameters.
        Default parameters: {"track_limit_per_playlist": 20, "lowest_popularity_for_best_songs": 95, "max_playlists": 5}
        """
        self.parameters = (
            parameters
            if parameters
            else {"track_limit_per_playlist": 20, "lowest_popularity_for_best_songs": 95, "max_playlists": 3}
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

    def predict(self, X):
        kmeans = KMeans(n_clusters=10, init='k-means++', n_init='auto')
        tracks_data = pd.read_json(TRACKS_PATH, lines=True)

        labels = kmeans.fit(X)
        tracks = list()
        for index, row in tracks_data.iterrows():
            tracks.append(Track(row["id"], row["popularity"], labels.labels_[index]))

        sorted_tracks = self.sort_tracks(tracks)
        best_groups = self.get_most_popular_groups(popularity=self.parameters["lowest_popularity_for_best_songs"], tracks=sorted_tracks)
        return self.make_playlists(sorted_tracks, best_groups)

    @staticmethod
    def sort_tracks(tracks):
        sorted_tracks = dict()
        for track in tracks:
            if track.group not in sorted_tracks:
                sorted_tracks[track.group] = list()
            sorted_tracks[track.group].append(track)
        return sorted_tracks

    @staticmethod
    def get_most_popular_groups(popularity, tracks):
        best_groups = set()
        for group, grouped_track in tracks.items():
            for track in grouped_track:
                if track.popularity >= popularity:
                    best_groups.add(group)
        return best_groups

    def make_playlists(self, tracks, groups):
        playlists = list()
        i = 0
        for group in groups:
            if i >= self.parameters["max_playlists"]:
                break
            new_playlist = Playlist()
            random_tracks = random.sample(tracks[group], self.parameters["track_limit_per_playlist"])
            for track in random_tracks:
                new_playlist.add(track)
            playlists.append(new_playlist)
            i += 1

        return playlists


if __name__ == "__main__":
    stats_data = pd.read_json(STATS_PATH, lines=True)
    model = AdvancedModel()
    corrected_data = stats_data.drop(columns=["track_id", "genre"]).drop_duplicates(keep="first")
    playlists = model.predict(corrected_data)

    for playlist in playlists:
        print(f"  Size: {playlist.size}")
        print(f"  Sum: {playlist.sum}")
        print(f"  Min Popularity: {playlist.min}")
        print(f"  Max Popularity: {playlist.max}")
        print(f"  Mean Popularity: {playlist.mean:.2f}")
        print("-" * 30)
