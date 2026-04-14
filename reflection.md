# Reflection: Profile Comparisons

This file compares the outputs of different user profiles run through the recommender.
The goal is to explain, in plain language, what changed between profiles and why it makes sense.

---

## Pair 1 — High-Energy Pop vs. Chill Lofi

**Pop profile:** genre=pop, mood=happy, energy=0.80  
**Lofi profile:** genre=lofi, mood=chill, energy=0.38

The pop profile returned Sunrise City at the top, followed by Gym Hero. Both are pop songs
with high energy — that part felt right. But Gym Hero is a workout track, not a feel-good
pop song. It showed up because the computer only sees the word "pop" in the genre column and
a high energy number. It has no idea that "Gym Hero + intense" is a different emotional
experience from "Sunrise City + happy," even though they share a genre tag. Think of it like
a librarian who shelves every pop CD in the same section regardless of whether it's a beach
playlist or a pre-race hype mix.

The lofi profile returned Library Rain and Midnight Coding at the top — both quiet, acoustic,
low-energy tracks. This felt genuinely accurate. The shift between these two profiles is dramatic
and correct: pop pushes everything toward fast, energetic, bright sounds; lofi pulls everything
toward slow, warm, textured sounds. The recommender handles this contrast well because the catalog
has enough lofi songs to fill the top results with genuine matches.

---

## Pair 2 — Deep Intense Rock vs. Conflicting Mood + Energy

**Rock profile:** genre=rock, mood=intense, energy=0.90  
**Conflict profile:** genre=lofi, mood=chill, energy=0.92

The rock profile returned Storm Runner in first place by a wide margin — that result felt
completely right. The problem was what came after. Gym Hero ranked second (again) because its
mood tag says "intense," which matched the user's mood preference even though Gym Hero is a pop
song and nothing about it feels like rock. Iron Tide — an actual metal track — ranked third,
which felt more correct for a rock listener but scored lower because its mood label is "angry"
rather than "intense." One word of difference between two nearly identical emotional states cost
Iron Tide an entire mood-match point.

The conflicting profile (chill mood, but maximum energy target) was designed to trick the system.
The expectation was that the high energy target would pull the results toward intense, loud songs.
But lofi songs still dominated the top results. Why? Because genre and mood together are worth
two full points, and even after being penalised for mismatched energy, Library Rain still
outscored energetic songs that had zero genre or mood connection to the profile. The system
was not tricked — it was stubborn. Whether that stubbornness is a feature or a flaw depends
on how you interpret the user's intent: if they genuinely want chill music, the result is good;
if their high-energy target was the real signal, the result ignores it.

---

## Pair 3 — Genre Not in Catalog vs. Opposing Genre + Mood

**Missing genre profile:** genre=jazz-fusion, mood=happy, energy=0.75  
**Opposing profile:** genre=metal, mood=relaxed, energy=0.55

When the genre does not exist in the catalog at all (jazz-fusion), every song receives zero
genre points. The recommender falls back entirely on mood and energy. For this profile, happy
songs with energy around 0.75 floated to the top — Rooftop Lights and Sunrise City appeared,
which are genuinely upbeat and appropriately energetic. Oddly, removing genre from the equation
produced *more intuitive* results for some positions, because energy and mood alone pulled in
songs that felt right even across different genres. This suggests that when the catalog is small,
genre matching can actually hurt diversity by locking too many points onto a label that may not
have enough songs behind it.

The opposing profile (metal but relaxed) had no perfect answer in the catalog — no song is
simultaneously metal and relaxed. The recommender had to choose: reward the genre match
(Iron Tide, metal/angry) or the mood match (Coffee Shop Stories, jazz/relaxed). Since genre
is worth one point and mood is also worth one point in the current weighted version, the
tiebreaker was energy. Iron Tide's energy (0.97) is further from the target (0.55) than Coffee
Shop Stories' energy (0.37), so Coffee Shop Stories ranked higher. A jazz café track beat a
metal song for a self-described metal listener. This result feels wrong — but the math was
consistent. It reveals that when genre and mood point in opposite directions and neither wins
outright, energy becomes the deciding factor, which is not always musically meaningful.

---

## Pair 4 — Standard Rock vs. After Weight Shift (genre halved, energy doubled)

**Before:** genre=+1.0 (was +2.0), mood=+1.0, energy=0–2.0 (was 0–1.0)

The most interesting change from the weight shift was in the rock profile. Before the shift,
Iron Tide (metal/angry) ranked third because it had no genre or mood match and only earned
energy points. After doubling the energy multiplier, Iron Tide's proximity to the target energy
of 0.90 (its actual energy is 0.97) earned it nearly 1.86 points from energy alone — enough
to jump above Gym Hero into second place.

This felt like an improvement. An intense, high-energy metal track is a much better
recommendation for someone who wants loud rock music than an upbeat pop gym track is,
regardless of what their mood label says. The weight shift made the system more responsive to
*how the music actually sounds* (energy) and less locked into genre labels. The tradeoff is
that two lofi songs with identical genre and mood labels but slightly different energies will
now rank further apart than before — energy differences that used to feel like a rounding
detail now carry real weight in the final score.

---

## Summary

| Profile Pair | Key Difference | Why It Makes Sense |
|---|---|---|
| Pop vs. Lofi | Fast/bright vs. slow/warm | Genre and energy pull opposite directions cleanly |
| Rock vs. Conflict | Clear match vs. stubborn genre lock | Genre+mood resist energy override — stable but inflexible |
| Missing Genre vs. Opposing | Fallback to mood+energy vs. no winner | Small catalog makes genre absence sometimes helpful |
| Rock before/after weight shift | Iron Tide rises above Gym Hero | Doubling energy rewarded sonic similarity over label matching |
