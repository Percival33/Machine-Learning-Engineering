from src.models.base_model import BaseModel
from src.models.advanced_model import AdvancedModel
import os
import pandas as pd

STATS_PATH = "file://" + os.path.abspath(
    os.path.join(
        __file__, "..", "..", "..", "data", "processed", "exploded_genres_with_stats.jsonl"
    )
)

POPULARITY_PATH = "file://" + os.path.abspath(
    os.path.join(
        __file__, "..", "..", "..", "data", "processed", "exploded_genres_with_popularity.jsonl"
    )
)


def compare():
    stats_data = pd.read_json(STATS_PATH, lines=True)
    popularity_data = pd.read_json(POPULARITY_PATH, lines=True)
    corrected_data = stats_data.drop(columns=["track_id", "genre"]).drop_duplicates(
        keep="first"
    )

    track_limit = 10

    advanced_model = AdvancedModel(track_limit_per_playlist=track_limit)
    base_model = BaseModel(track_limit_per_playlist=track_limit)

    base_playlists = base_model.predict(popularity_data)
    advanced_playlists = advanced_model.predict(corrected_data)

    base_results = []
    for _, playlist in base_playlists.items():
        base_results.append(
            {
                "size": playlist.size,
                "min_track_popularity": playlist.min,
                "max_track_popularity": playlist.max,
                "mean_popularity": f"{playlist.mean:.2f}",
                "tracks": [track.to_json_serializable() for track in playlist.tracks],
                "retention": playlist.get_retention()
            }
        )

    advanced_results = []
    for playlist in advanced_playlists:
        advanced_results.append(
            {
                "size": playlist.size,
                "min_track_popularity": playlist.min,
                "max_track_popularity": playlist.max,
                "mean_popularity": f"{playlist.mean:.2f}",
                "tracks": [track.to_json_serializable() for track in playlist.tracks],
                "retention": playlist.get_retention()
            }
        )

    print(base_results)
    print(advanced_results)


if __name__ == "__main__":
    compare()