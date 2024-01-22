import pandas as pd
from pandas import DataFrame
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data")
OUTPUT_FOLDER = f"{DATA_DIR}/processed"


def agg_events(x):
    return tuple(x)


def track_stats_per_user(tracks_df: DataFrame):
    session_df = pd.read_json(
        os.path.join(DATA_DIR, "raw", "05_02_v2", "sessions.jsonl"), lines=True
    )
    tracks_tmp = tracks_df[["id", "duration_ms"]]
    session_tmp = session_df.sort_values(by=["session_id", "timestamp"], ascending=[True, True])

    session_tmp["time_played"] = (
        pd.to_datetime(session_tmp["timestamp"]).diff().dt.total_seconds() * 1000
    )
    session_tmp["time_played"] = session_tmp["time_played"].shift(-1)

    track_minutes_played = (
        session_tmp.groupby(["track_id", "user_id"])["time_played"].agg("sum").reset_index()
    )
    grouped_events = (
        session_tmp.groupby(["track_id", "user_id"])["event_type"].agg([agg_events]).reset_index()
    )

    track_user_stats = pd.merge(
        track_minutes_played, tracks_tmp, how="left", left_on="track_id", right_on="id"
    )
    track_user_stats = pd.merge(
        track_user_stats, grouped_events, how="left", on=["track_id", "user_id"]
    )

    track_user_stats["percentage_played"] = (
        track_user_stats["time_played"] / track_user_stats["duration_ms"] * 100
    )
    track_user_stats["percentage_played"] = track_user_stats.apply(
        lambda row: 100.0 if row.percentage_played > 100 else row.percentage_played, axis=1
    )
    track_user_stats["was_liked"] = track_user_stats.apply(
        lambda row: "like" in row.agg_events, axis=1
    )
    track_user_stats["was_skipped"] = track_user_stats.apply(
        lambda row: "skip" in row.agg_events, axis=1
    )

    track_user_stats = track_user_stats.drop(columns=["id", "agg_events"])
    track_user_stats = track_user_stats.drop(
        track_user_stats[
            abs(track_user_stats.time_played) / 10 > track_user_stats.duration_ms
        ].index
    )
    track_user_stats = track_user_stats.drop(
        track_user_stats[track_user_stats.time_played == 0.0].index
    )

    track_user_stats.to_json(
        os.path.join(OUTPUT_FOLDER, "track_user_stats.jsonl"),
        orient="records",
        lines=True,
    )


if __name__ == "__main__":
    tracks_df = pd.read_json(os.path.join(DATA_DIR, "raw", "05_02_v2", "tracks.jsonl"), lines=True)

    # the following is done because some of the songs have identical statistics
    # they interfere in the generating process, but also there are only like 50 of them, so we just cut them out
    tracks_df = tracks_df.drop_duplicates(
        keep="first",
        subset=[
            "popularity",
            "danceability",
            "energy",
            "key",
            "loudness",
            "speechiness",
            "acousticness",
            "instrumentalness",
            "liveness",
            "valence",
            "tempo",
        ],
    )

    tracks_df.to_json(
        os.path.join(OUTPUT_FOLDER, "tracks_no_duplicates.jsonl"),
        orient="records",
        lines=True,
    )

    artists_df = pd.read_json(
        os.path.join(DATA_DIR, "raw", "05_02_v2", "artists.jsonl"), lines=True
    )

    tracks_genre_df = tracks_df.merge(
        artists_df[["id", "genres"]], left_on="id_artist", right_on="id", how="inner"
    )

    exploded_genres = tracks_genre_df[["id_x", "genres"]].explode("genres").reset_index()
    exploded_genres = exploded_genres.rename(columns={"id_x": "track_id", "genres": "genre"})
    exploded_genres.drop(columns=["index"])

    exploded_genres.to_json(
        os.path.join(OUTPUT_FOLDER, "exploded_genres.jsonl"), orient="records", lines=True
    )

    exploded_genres_with_popularity = exploded_genres.drop(columns="index").merge(
        tracks_df[["id", "popularity"]], left_on="track_id", right_on="id"
    )
    exploded_genres_with_popularity.drop(columns="id").to_json(
        os.path.join(OUTPUT_FOLDER, "exploded_genres_with_popularity.jsonl"),
        orient="records",
        lines=True,
    )

    exploded_genres_with_stats = exploded_genres.drop(columns="index").merge(
        tracks_df[
            [
                "id",
                "popularity",
                "danceability",
                "energy",
                "key",
                "loudness",
                "speechiness",
                "acousticness",
                "instrumentalness",
                "liveness",
                "valence",
                "tempo",
            ]
        ],
        left_on="track_id",
        right_on="id",
    )

    exploded_genres_with_stats.drop(columns="id").to_json(
        os.path.join(OUTPUT_FOLDER, "exploded_genres_with_stats.jsonl"),
        orient="records",
        lines=True,
    )

    track_stats_per_user(tracks_df)
    print(f"dataset saved to a folder: {OUTPUT_FOLDER}")
