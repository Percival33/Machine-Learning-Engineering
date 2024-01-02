from collections import defaultdict

import pandas as pd
import os
from sklearn.cluster import KMeans

from src.domain.Playlist import Playlist
from src.domain.Track import Track
from src.models.ABCSolver import AbstractSolver

DATA_PATH = os.path.abspath(
    os.path.join(".", "..", "..", "data", "processed", "exploded_genres_with_stats.jsonl")
)


class AdvancedModel(AbstractSolver):
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

    def predict(self, X):
        kmeans = KMeans(n_clusters=10, init='k-means++', n_init='auto')
        labels = kmeans.fit(X)
        return labels.labels_


if __name__ == "__main__":
    data = (pd.read_json(DATA_PATH, lines=True)
            .drop(columns=["track_id", "genre"])).drop_duplicates(keep=False)
    model = AdvancedModel()
    model.predict(data)
