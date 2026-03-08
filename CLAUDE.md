# Aggregate Dynasty Rankings — Project Context

## Overview
A fantasy sports dynasty rankings aggregator covering baseball, hockey, basketball, and football. The goal is to collect rankings from multiple sources per sport and combine them into a master file.

## Folder Structure
```
baseball/
  baseball_rankings_master.csv
  harryknowsball_players.csv   ← raw HarryKnowsBall source data
hockey/
  hockey_skaters_master.csv    ← skaters (F and D) only
  hockey_goalies_master.csv    ← goalies (G) only
basketball/
  basketball_rankings_master.csv
football/
  football_rankings_master.csv
scripts/
  recalculate.py               ← shared calc script for any sport
```

## Key Files
- `<sport>/<sport>_rankings_master.csv` — main working file per sport. Wide format: one row per player, each ranking source as its own column.
- `baseball/harryknowsball_players.csv` — raw HarryKnowsBall crowdsourced rankings (Rank, Name, Value, Age, Positions, Team, Level).
- `hockey/hockey_skaters_master.csv` — skaters master (F and D positions).
- `hockey/hockey_goalies_master.csv` — goalies master (G position).

## Data Format (rankings_master files)
Columns: `Player, Position, Team, Age, Level, ETA`, then one column per ranking source in the format `"Source (Author, Date)"`, then `Average Rank, Rank Variance`.

**Hockey is an exception** — skaters and goalies are in separate files, and the column format is slimmer: `Player, Position, Age`, then source columns, then `Average Rank, Rank Variance`. No Team, Level, or ETA columns.

Each sport has its own set of ranking sources (different outlets/authors per sport).

## Calculated Columns
- **Average Rank** — mean of all available source rankings for a player (ignores sources that don't include the player)
- **Rank Variance** — coefficient of variation: `STDDEV / (mean + 5)`; blank if only one source covers the player

## Recalculating Stats
Run the shared script after adding or updating any source column:
```
python3 scripts/recalculate.py baseball/baseball_rankings_master.csv
python3 scripts/recalculate.py hockey/hockey_skaters_master.csv
python3 scripts/recalculate.py hockey/hockey_goalies_master.csv
```

## Source Columns Per Sport

**Baseball** (5 sources): FantraxHQ, HarryKnowsBall, The Athletic, RotoWorld, FantasyPros

**Football** (6 sources): PFF (Nathan Jahnke), KeepTradeCut (Crowdsourced), FantasyPros, DraftSharks, Dynasty League Football (Crowdsourced), FantasyCalc (Crowdsourced, Mar 2026)

**Basketball** (5 sources, 316 players, 273 with multi-source averages):
- `Dizzle Dynasty (Cat, Mar 2026)` — category leagues, 213 players (may be truncated)
- `Noah Rubin (Cat, Jan 2026)` — category leagues, 250 players
- `Matt Lawson (Pts, Mar 2026)` — points leagues, 300 players
- `Hashtag Basketball (Pts, Feb 2026)` — points leagues, 250 players (by Joseph Mamone)
- `RoundBallRhettoric (Pts, Mar 2026)` — points leagues, 228 players

**Hockey Skaters** (3 sources, ~370 players, ~254 with multi-source averages):
- `Dobber (Mar 2026)` — 300 players; "y" flag in source = defenseman
- `Hashtag Hockey (Mar 2026)` — 200 players (skaters only)
- `Lineup Experts (Oct 2025)` — 310 skaters extracted from combined 350-player list (skaters + goalies); overall ranks preserved (includes goalie rank slots)

**Hockey Goalies** (3 sources, 70 goalies, 44 with multi-source averages):
- `Dobber (Mar 2026)` — 60 goalies
- `Hashtag Hockey (Mar 2026)` — 50 goalies
- `Lineup Experts (Oct 2025)` — 34 goalies extracted from combined list

Hockey merge scripts: `create_dobber_hockey_skaters.py`, `create_dobber_hockey_goalies.py`, `merge_hashtag_hockey_skaters.py`, `merge_hashtag_hockey_goalies.py`, `merge_lineup_experts_hockey_skaters.py`, `merge_lineup_experts_hockey_goalies.py`

## Basketball-Specific Format
Basketball source column headers include a league format indicator: `"Source (Format, Date)"` where Format is `Cat` (category), `Pts` (points), or `Unk` (unknown). This is in addition to the standard date field.

Basketball `Level` values: `NBA` for active/drafted pros, `College` for college prospects.

## Adding a New Source
1. Parse raw data into rank/player/pos/team
2. Match players by normalized name to existing rows (strip Jr./Sr./II/III/IV, periods, apostrophes, lowercase)
3. Add unmatched players as new rows
4. Run `recalculate.py` to update Average Rank and Rank Variance

For basketball and hockey, use a short Python merge script (see `scripts/merge_*_basketball.py` and `scripts/merge_*_hockey_*.py` for examples): read master CSV, build a dict of normalized_name→row, update existing rows, append new players, write back, then run recalculate.py.

**Name normalization** (`normalize()` function used in all merge scripts):
```python
import unicodedata, re
def normalize(name):
    name = unicodedata.normalize("NFKD", name)
    name = name.encode("ascii", "ignore").decode("ascii")
    name = name.lower()
    name = re.sub(r"\b(jr|sr|ii|iii|iv|v)\b\.?", "", name)
    name = re.sub(r"[^a-z\s]", "", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name
```
This handles accented characters automatically (Jokić→jokic, Dončić→doncic, Porziņģis→porzingis, etc.).

Common basketball canonical name conventions (use these in master, not source variants):
- "Alex Sarr" (not "Alexandre Sarr")
- "Bub Carrington" (not "Carlton Carrington")
- "Ronald Holland II" (not "Ron Holland II")
- "Nic Claxton" (not "Nicolas Claxton")

Basketball merge scripts: `merge_lawson_basketball.py`, `merge_hashtag_basketball.py`, `merge_roundballrhettoric_basketball.py`

Common hockey name mismatches to watch for across sources:
- "JJ Peterka" (canonical) vs "John-Jason Peterka" (Lineup Experts)
- "Matty Beniers" (canonical) vs "Matthew Beniers" (Hashtag)
- "Zack Bolduc" (canonical) vs "Zachary Bolduc" (Lineup Experts)
- "Matt Coronato" (canonical) vs "Matthew Coronato" (Lineup Experts)
- "Arseniy Gritsyuk" (canonical) vs "Arseny Gritsyuk" (Lineup Experts)
- "Jonathan Marchessault" (canonical) vs "Jon Marchessault" (Lineup Experts)
- "Mackie Samoskevich" (canonical) vs "Matthew Samoskevich" (Lineup Experts)
- "Josh Norris" (canonical) vs "Joshua Norris" (Lineup Experts)
- "Zach Benson" (canonical) vs "Zachary Benson" (Lineup Experts)

Common name mismatches to watch for across football sources:
- "Cam Ward" (canonical) vs "Cameron Ward" (DraftSharks)
- "James Cook III" (canonical) vs "James Cook" (DraftSharks/KTC)
- "Travis Etienne Jr." (canonical) vs "Travis Etienne" (DraftSharks)
- "Cam Skattebo" (canonical) vs "Cameron Skattebo" (DraftSharks)
- "Chigoziem Okonkwo" (canonical) vs "Chig Okonkwo" (FantasyPros/DLF)

## Notes
- `rankings.csv` was deleted (was a long-format duplicate, not needed).
- KTC data was cut off at rank 250 (more may exist beyond that).
- Football master includes ~313 players across 6 sources. Age populated from FantasyCalc (205 players).
- Basketball Dizzle Dynasty source (Mar 2026) was truncated at rank 213 — may be incomplete.
- Basketball master has 5 sources and 316 players as of Mar 2026.
- Hockey skaters master has 3 sources and ~370 players as of Mar 2026.
- Hockey goalies master has 3 sources and 70 players as of Mar 2026.
- Lineup Experts hockey source is from Oct 2025 (older than Dobber/Hashtag); skater ranks are overall (includes goalie rank slots in the gaps); goalie ranks are converted to goalie-only ranks 1–34 (by their order of appearance in the combined list).
- `hockey_rankings_master.csv` is now unused/empty — hockey is split into skaters and goalies files.
