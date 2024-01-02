import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data")
OUTPUT_FOLDER = f"{DATA_DIR}/processed"

if __name__ == "__main__":
    tracks_df = pd.read_json(os.path.join(DATA_DIR, "raw", "05_02_v2", "tracks.jsonl"), lines=True)
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
            ["id",
             "danceability",
             "energy",
             "key",
             "loudness",
             "speechiness",
             "acousticness",
             "instrumentalness",
             "liveness",
             "valence",
             "tempo"]
        ],
        left_on="track_id", right_on="id"
    )

    exploded_genres_with_stats.drop(columns="id").to_json(
        os.path.join(OUTPUT_FOLDER, "exploded_genres_with_stats.jsonl"),
        orient="records",
        lines=True,
    )
    print(f"dataset saved to a folder: {OUTPUT_FOLDER}")
