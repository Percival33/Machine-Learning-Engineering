from dataclasses import dataclass


@dataclass(frozen=True)
class Track:
    track_id: str
    popularity: int
    group: int

    def to_json_serializable(self):
        return self.track_id
