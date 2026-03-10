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
- **Rank Variance** — coefficient of variation: `sample_stddev / (mean + 5)`; blank if only one source covers the player. The `+5` dampening prevents inflation for top-ranked players.

## Recalculating Stats
Run the shared script after adding or updating any source column:
```
python3 scripts/recalculate.py baseball/baseball_rankings_master.csv
python3 scripts/recalculate.py basketball/basketball_rankings_master.csv
python3 scripts/recalculate.py football/football_rankings_master.csv
python3 scripts/recalculate.py hockey/hockey_skaters_master.csv
python3 scripts/recalculate.py hockey/hockey_goalies_master.csv
```

## Source Columns Per Sport

**Baseball** (7 sources, 672 players, 530 with multi-source averages):
- `FantraxHQ_Roto (Wes Hughes, 2026-02-23)` — 400 players
- `HarryKnowsBall (Crowdsourced, 2026-03-03)` — 489 players
- `The Athletic (Chris Welsh, 2026-02-27)` — 400 players
- `RotoWorld (Eric Cross, 2026-01-15)` — 200 players
- `FantasyPros (FantasyPros, 2026-03-03)` — 300 players
- `Baseball America (Feb 2026)` — 500 players
- `Owen FBB Invitational (Startup, Feb 2026)` — 499 players (overall pick number as rank)

**Football** (6 sources, 313 players, 258 with multi-source averages):
- `PFF (Nathan Jahnke, 2026-02)` — 200 players
- `KeepTradeCut (Crowdsourced, 2026-03)` — 227 players (cut off at rank 250)
- `FantasyPros (FantasyPros, 2026-03)` — 250 players
- `DraftSharks (DraftSharks, 2026-03)` — 200 players
- `Dynasty League Football (Crowdsourced, 2026-02-04)` — 250 players
- `FantasyCalc (Crowdsourced, 2026-03)` — 250 players

**Basketball** (5 sources, 316 players, 273 with multi-source averages):
- `Dizzle Dynasty (Cat, Mar 2026)` — category leagues, 213 players (may be truncated)
- `Noah Rubin (Cat, Jan 2026)` — category leagues, 250 players
- `Matt Lawson (Pts, Mar 2026)` — points leagues, 300 players
- `Hashtag Basketball (Pts, Feb 2026)` — points leagues, 250 players (by Joseph Mamone)
- `RoundBallRhettoric (Pts, Mar 2026)` — points leagues, 228 players

**Hockey Skaters** (4 sources, 400 players, 330 with multi-source averages):
- `Dobber (Mar 2026)` — 300 players
- `Hashtag Hockey (Mar 2026)` — 199 players (skaters only)
- `Lineup Experts (Oct 2025)` — 310 skaters from combined 350-player list; re-ranked sequentially 1–310
- `ErockThud (Mar 2026)` — 333 skaters from combined list (also includes goalies + draft picks); re-ranked sequentially 1–333

**Hockey Goalies** (5 sources, 69 goalies, 44 with multi-source averages):
- `Dobber (Mar 2026)` — 60 goalies
- `Hashtag Hockey (Mar 2026)` — 50 goalies
- `Lineup Experts (Oct 2025)` — 34 goalies; re-ranked sequentially 1–34
- `ErockThud (Mar 2026)` — 34 goalies; re-ranked sequentially 1–34
- `RankKing (Mar 2026)` — 40 goalies (added from mobile app screenshots)

For combined hockey sources (Lineup Experts, ErockThud): skaters and goalies are split into their respective master files and each group is re-ranked sequentially 1–N by their order of appearance in the original combined list.

Hockey merge scripts: `create_dobber_hockey_skaters.py`, `create_dobber_hockey_goalies.py`, `merge_hashtag_hockey_skaters.py`, `merge_hashtag_hockey_goalies.py`, `merge_lineup_experts_hockey_skaters.py`, `merge_lineup_experts_hockey_goalies.py`, `merge_erock_hockey.py`, `merge_rankking_hockey_goalies.py`

## Basketball-Specific Format
Basketball source column headers include a league format indicator: `"Source (Format, Date)"` where Format is `Cat` (category), `Pts` (points), or `Unk` (unknown).

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

Common hockey name mismatches to watch for across sources:
- "JJ Peterka" (canonical) vs "John-Jason Peterka" (Lineup Experts / ErockThud)
- "Matty Beniers" (canonical) vs "Matthew Beniers" (Hashtag / ErockThud)
- "Zack Bolduc" (canonical) vs "Zachary Bolduc" (Lineup Experts / ErockThud)
- "Matt Coronato" (canonical) vs "Matthew Coronato" (Lineup Experts / ErockThud)
- "Arseniy Gritsyuk" (canonical) vs "Arseny Gritsyuk" (Lineup Experts / ErockThud)
- "Jonathan Marchessault" (canonical) vs "Jon Marchessault" (Lineup Experts / ErockThud)
- "Mackie Samoskevich" (canonical) vs "Matthew Samoskevich" (Lineup Experts / ErockThud)
- "Josh Norris" (canonical) vs "Joshua Norris" (Lineup Experts / ErockThud)
- "Zach Benson" (canonical) vs "Zachary Benson" (Lineup Experts / ErockThud)
- "Matt Boldy" (canonical) vs "Matthew Boldy" (ErockThud)
- "Gabe Perreault" (canonical) vs "Gabriel Perreault" (ErockThud)
- "Matt Savoie" (canonical) vs "Matthew Savoie" (ErockThud)

Common name mismatches to watch for across football sources:
- "Cam Ward" (canonical) vs "Cameron Ward" (DraftSharks)
- "James Cook III" (canonical) vs "James Cook" (DraftSharks/KTC)
- "Travis Etienne Jr." (canonical) vs "Travis Etienne" (DraftSharks)
- "Cam Skattebo" (canonical) vs "Cameron Skattebo" (DraftSharks)
- "Chigoziem Okonkwo" (canonical) vs "Chig Okonkwo" (FantasyPros/DLF)

## Website (GitHub Pages)
The data is published as a static site at the repo's GitHub Pages URL. The entry point is `index.html` in the root.

- Tabbed interface: Baseball, Football, Basketball, Hockey (Skaters), Hockey (Goalies)
- Each tab lazy-loads its CSV on first click; baseball loads immediately on page open
- Active tab has a sport-colored background fill; the page background also shifts to the sport's theme color
  - Baseball = light blue, Football = light green, Basketball = light orange, Hockey = light purple
- Rank Variance column uses a green→yellow→red cell background gradient (0.0 = green, 0.5+ = red)
- Positions displayed as plain text (no color coding)
- **Hidden columns**: Level and ETA are hidden from baseball, basketball, and football tables (present in CSVs but not displayed)
- Hockey has no Level/ETA/Team columns in the CSV at all
- CSV parsing uses Papa Parse with `header: false` + manual field extraction to avoid a known Papa Parse bug with certain CRLF files
- **Weight row**: a second `<thead>` row shows a number input (default 1) below each source column. Changing a weight dynamically recomputes a weighted average (`Σ rank×weight / Σ weight`, skipping blank ranks) and re-sorts the table. Weights are session-only (reset on refresh). `stopPropagation()` on input clicks prevents DataTables from treating them as column sort clicks.

## Football-Specific Notes
- Age data source: FantasyCalc (Mar 2026) — stored as decimal (e.g. 24.1); blank for rookies
- Merge script for new football sources: `scripts/merge_fantasycalc_football.py` (use as template)
- When adding a new football source, also backfill Age if the source provides it and the player's Age is currently blank

## Hockey-Specific Notes
- Age column populated from a 500-player ranked list (ages as of Oct 2025); ~346 skaters and ~46 goalies have ages. Players not in that list remain blank. Script: `scripts/add_hockey_ages.py`.
- Lineup Experts source is from Oct 2025 (older than the other three sources).
- ErockThud source had a typo: "Artyom Levhunov" → correct is "Artyom Levshunov"; handled in NAME_MAP.
- RankKing source uses "Samuel Montembeault" → mapped to canonical "Sam Montembeault" via NAME_MAP in merge script.

## Miscellaneous Notes
- `rankings.csv` was deleted (was a long-format duplicate, not needed).
- `hockey_rankings_master.csv` is now unused/empty — hockey is split into skaters and goalies files.
- Baseball positions normalized: RF/CF/LF → OF; multi-position → first only.
- Basketball positions normalized: PF → F, PF/C → F.
- Hockey skater positions normalized: LW/RW/C → F (all forwards use F).
