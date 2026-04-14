"""
Command line runner for the Music Recommender Simulation.

Run from the project root with:
    python3 -m src.main

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    from src.recommender import load_songs, recommend_songs, SCORING_MODES
except ModuleNotFoundError:
    from recommender import load_songs, recommend_songs, SCORING_MODES


def print_recommendations(
    label: str,
    user_prefs: dict,
    songs: list,
    k: int = 5,
    mode: str = "balanced",
) -> None:
    """Print a formatted recommendations block for one profile and scoring mode."""
    recommendations = recommend_songs(user_prefs, songs, k=k, mode=mode)
    max_score = SCORING_MODES[mode].max_score
    width = 64
    genre  = user_prefs.get("genre", "?")
    mood   = user_prefs.get("mood", "?")
    energy = user_prefs.get("target_energy", "?")

    print()
    print("=" * width)
    print(f"  {label}  [mode: {mode}]")
    print(f"  genre={genre} | mood={mood} | target_energy={energy}")
    print("=" * width)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n  #{rank}  {song['title']} — {song['artist']}")
        print(f"       Score : {score} / {max_score}")
        print(f"       Why   : {explanation}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # -----------------------------------------------------------------------
    # Scoring mode — change this one line to switch the ranking strategy
    #   "genre_first"    genre=2.5, mood=0.5, energy=0–1.0   max=4.0
    #   "mood_first"     genre=0.5, mood=2.5, energy=0–1.0   max=4.0
    #   "energy_focused" genre=0.5, mood=0.5, energy=0–3.0   max=4.0
    #   "balanced"       genre=1.0, mood=1.0, energy=0–2.0   max=4.0
    # -----------------------------------------------------------------------
    ACTIVE_MODE = "balanced"

    # -----------------------------------------------------------------------
    # Standard profiles
    # -----------------------------------------------------------------------

    # High-Energy Pop: upbeat, radio-friendly, strong positive energy
    profile_pop = {
        "genre":         "pop",
        "mood":          "happy",
        "target_energy": 0.80,
    }

    # Chill Lofi: studying, low stimulation, warm acoustic texture
    profile_lofi = {
        "genre":         "lofi",
        "mood":          "chill",
        "target_energy": 0.38,
    }

    # Deep Intense Rock: maximum activation, raw electric energy
    profile_rock = {
        "genre":         "rock",
        "mood":          "intense",
        "target_energy": 0.90,
    }

    # -----------------------------------------------------------------------
    # Adversarial / edge-case profiles
    # -----------------------------------------------------------------------

    # Edge Case 1 — Conflicting mood + energy
    # mood says "chill" but energy target is near-maximum (0.92).
    # Exposes: the system will grant mood points to lofi songs but then
    # heavily penalise them on energy, possibly ranking an intense song higher.
    profile_conflict = {
        "genre":         "lofi",
        "mood":          "chill",
        "target_energy": 0.92,
    }

    # Edge Case 2 — Genre that does not exist in the catalog
    # "jazz-fusion" matches nothing, so genre contributes 0 pts to every song.
    # Exposes: the recommender falls back entirely on mood + energy similarity,
    # revealing what a genre-less ranking looks like.
    profile_missing_genre = {
        "genre":         "jazz-fusion",
        "mood":          "happy",
        "target_energy": 0.75,
    }

    # Edge Case 3 — Opposing genre and mood pairing
    # "metal" is inherently intense; "relaxed" is its opposite.
    # No song in the catalog has both. Forces the scorer to choose between
    # a genre match (Iron Tide) or a mood match (Coffee Shop Stories).
    profile_mismatch = {
        "genre":         "metal",
        "mood":          "relaxed",
        "target_energy": 0.55,
    }

    # Edge Case 4 — Dead-centre energy target
    # target_energy=0.50 sits in the middle of the 0–1 scale, so every song
    # earns a middling energy score (roughly 0.4–0.6 pts) regardless of its
    # actual energy. Genre and mood become the only real differentiators.
    profile_neutral_energy = {
        "genre":         "ambient",
        "mood":          "chill",
        "target_energy": 0.50,
    }

    # -----------------------------------------------------------------------
    # Run all profiles using the active mode
    # -----------------------------------------------------------------------
    profiles = [
        ("Standard — High-Energy Pop",                    profile_pop),
        ("Standard — Chill Lofi",                         profile_lofi),
        ("Standard — Deep Intense Rock",                  profile_rock),
        ("Edge Case 1 — Conflicting Mood + Energy",       profile_conflict),
        ("Edge Case 2 — Genre Not in Catalog",            profile_missing_genre),
        ("Edge Case 3 — Opposing Genre + Mood",           profile_mismatch),
        ("Edge Case 4 — Dead-Centre Energy Target",       profile_neutral_energy),
    ]

    for label, prefs in profiles:
        print_recommendations(label, prefs, songs, k=5, mode=ACTIVE_MODE)

    # -----------------------------------------------------------------------
    # Mode comparison — same pop profile through all four strategies
    # Shows how ranking strategy changes the results for the same user
    # -----------------------------------------------------------------------
    print("\n" + "#" * 64)
    print("  MODE COMPARISON — High-Energy Pop across all strategies")
    print("#" * 64)

    for mode_name in SCORING_MODES:
        print_recommendations(
            f"Pop profile",
            profile_pop,
            songs,
            k=3,
            mode=mode_name,
        )


if __name__ == "__main__":
    main()
