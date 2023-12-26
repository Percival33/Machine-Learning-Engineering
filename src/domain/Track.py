from dataclasses import dataclass


@dataclass(frozen=True)
class Track:
    track_id: str
    popularity: int
