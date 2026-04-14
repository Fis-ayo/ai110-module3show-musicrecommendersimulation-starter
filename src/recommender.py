from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k Song objects ranked by score against the given UserProfile."""
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a plain-language string describing why a Song matches a UserProfile."""
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences (+2.0 genre, +1.0 mood, +0–1 energy); return (score, reasons)."""
    score = 0.0
    reasons = []

    # Rule 1 — Genre match: +2.0 points
    if song["genre"] == user_prefs.get("genre", ""):
        score += 2.0
        reasons.append(f"genre match (+2.0)")

    # Rule 2 — Mood match: +1.0 point
    if song["mood"] == user_prefs.get("mood", ""):
        score += 1.0
        reasons.append(f"mood match (+1.0)")

    # Rule 3 — Energy similarity: +0.0 to +1.0 points
    # Rewards closeness to the user's target, not a high or low absolute value.
    # A song at 0.40 scores 0.98 for a user targeting 0.38.
    # A song at 0.91 scores only 0.47 for that same user.
    target_energy = user_prefs.get("target_energy", 0.5)
    energy_points = round(1.0 - abs(song["energy"] - target_energy), 2)
    score += energy_points
    reasons.append(f"energy {song['energy']} vs target {target_energy} (+{energy_points})")

    return round(score, 2), reasons


def load_songs(csv_path: str) -> List[Dict]:
    """Parse a CSV file of songs and return a list of dicts with typed numeric fields."""
    import csv
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort by score descending, and return the top k as (song, score, explanation) tuples."""
    # Step 1 — score every song in the catalog
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, "; ".join(reasons)))

    # Step 2 & 3 — sort by score descending, return top k
    # sorted() is used here instead of .sort() because:
    #   sorted() returns a NEW list, leaving `scored` unchanged.
    #   .sort() sorts IN PLACE and returns None — chaining [:k] onto it would fail.
    return sorted(scored, key=lambda item: item[1], reverse=True)[:k]
