from src.models.base_model import BaseModel
from src.models.advanced_model import AdvancedModel
from src.domain.Playlist import Playlist
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


def get_model_results(playlists: list[Playlist]) -> dict[str, float]:
    results = {
        "size": 0,
        "min_track_popularity": 0,
        "max_track_popularity": 0,
        "mean_popularity": 0,
        "retention": 0,
    }

    for playlist in playlists:
        results["size"] += playlist.size
        results["min_track_popularity"] += playlist.min
        results["max_track_popularity"] += playlist.max
        results["mean_popularity"] += playlist.mean
        results["retention"] += playlist.get_retention()

    results["size"] = results["size"] / len(playlists)
    results["min_track_popularity"] = results["min_track_popularity"] / len(playlists)
    results["max_track_popularity"] = results["max_track_popularity"] / len(playlists)
    results["mean_popularity"] = results["mean_popularity"] / len(playlists)
    results["retention"] = results["retention"] / len(playlists)

    return results


def compress_dicts(dicts: list[dict[str, float]]) -> dict[str, float]:
    results = {
        "size": 0,
        "min_track_popularity": 0,
        "max_track_popularity": 0,
        "mean_popularity": 0,
        "retention": 0,
    }

    for playlist in dicts:
        results["size"] += playlist["size"]
        results["min_track_popularity"] += playlist["min_track_popularity"]
        results["max_track_popularity"] += playlist["max_track_popularity"]
        results["mean_popularity"] += playlist["mean_popularity"]
        results["retention"] += playlist["retention"]

    results["size"] = results["size"] / len(dicts)
    results["min_track_popularity"] = results["min_track_popularity"] / len(dicts)
    results["max_track_popularity"] = results["max_track_popularity"] / len(dicts)
    results["mean_popularity"] = results["mean_popularity"] / len(dicts)
    results["retention"] = results["retention"] / len(dicts)

    return results


def compare():
    stats_data = pd.read_json(STATS_PATH, lines=True)
    popularity_data = pd.read_json(POPULARITY_PATH, lines=True)
    corrected_data = stats_data.drop(columns=["track_id", "genre"]).drop_duplicates(keep="first")

    track_limit = 10
    iterations = 10

    advanced_model = AdvancedModel(track_limit_per_playlist=track_limit)
    base_model = BaseModel(track_limit_per_playlist=track_limit)
    overall_results = dict()
    overall_results["base"] = list()
    overall_results["advanced"] = list()

    for _ in range(iterations):
        base_playlists = base_model.predict(popularity_data)
        advanced_playlists = advanced_model.predict(corrected_data)

        overall_results["base"].append(get_model_results(list(base_playlists.values())))
        overall_results["advanced"].append(get_model_results(advanced_playlists))

    overall_results["base"] = compress_dicts(overall_results["base"])
    overall_results["advanced"] = compress_dicts(overall_results["advanced"])

    return overall_results


if __name__ == "__main__":
    print(compare())
