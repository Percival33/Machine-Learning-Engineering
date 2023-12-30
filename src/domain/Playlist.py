from dataclasses import dataclass, field
from src.domain.Track import Track


@dataclass
class Playlist:
    tracks: list[Track] = field(default_factory=list)
    size: int = 0
    sum: int = 0
    min: int = float("inf")
    max: int = float("-inf")
    mean: float = 0.0
    MAX_SIZE: int = 20

    def __init__(self, max_size: int = 20):
        self.tracks = []
        self.size = 0
        self.sum = 0
        self.min = float("inf")
        self.max = float("-inf")
        self.mean = 0.0
        self.MAX_SIZE = max_size

    def limit(self):
        if self.size <= self.MAX_SIZE:
            return

        min_popularity_track = min(self.tracks, key=lambda x: x.popularity)
        self.tracks.remove(min_popularity_track)

        self.size -= 1
        self.sum -= min_popularity_track.popularity

        if self.tracks:
            self.min = min(track.popularity for track in self.tracks)
            self.max = max(track.popularity for track in self.tracks)
            self.mean = self.sum / self.size
        else:
            self.min = float("inf")
            self.max = float("-inf")
            self.mean = 0

    def add(self, current_track: Track):
        self.tracks.append(current_track)
        self.size += 1
        self.sum += current_track.popularity
        self.min = min(self.min, current_track.popularity)
        self.max = max(self.max, current_track.popularity)
        self.mean = self.sum / self.size
        self.limit()
