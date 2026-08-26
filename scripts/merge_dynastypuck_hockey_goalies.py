#!/usr/bin/env python3
"""
Merge Dynasty Puck (Aug 2026) goalie rankings into hockey_goalies_master.csv.
This is a new source: skaters are excluded here (see merge_dynastypuck_hockey_skaters.py).
Goalies are re-ranked sequentially 1-N among goalies only, by order of appearance
in the original combined 300-player list.
Run recalculate.py afterward.
"""

import csv
import os
import re
import subprocess
import unicodedata

MASTER_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "hockey", "hockey_goalies_master.csv"))
SOURCE_COL = "Dynasty Puck (Aug 2026)"

# (goalie_rank, name) — ranked 1-N by order of appearance in Dynasty Puck combined list
GOALIE_DATA = [
    (1, "Andrei Vasilevskiy"),
    (2, "Connor Hellebuyck"),
    (3, "Logan Thompson"),
    (4, "Jake Oettinger"),
    (5, "Igor Shesterkin"),
    (6, "Ilya Sorokin"),
    (7, "Spencer Knight"),
    (8, "Lukas Dostal"),
    (9, "Dustin Wolf"),
    (10, "Jeremy Swayman"),
    (11, "Jakub Dobes"),
    (12, "Jesper Wallstedt"),
    (13, "Karel Vejmelka"),
    (14, "Jet Greaves"),
    (15, "Yaroslav Askarov"),
    (16, "Juuse Saros"),
    (17, "Filip Gustavsson"),
    (18, "Mackenzie Blackwood"),
    (19, "Joel Hofer"),
    (20, "Linus Ullmark"),
    (21, "Jake Allen"),
    (22, "Ukko-Pekka Luukkonen"),
    (23, "Jacob Markstrom"),
    (24, "Brandon Bussi"),
    (25, "Daniel Vladar"),
    (26, "Sergei Bobrovsky"),
    (27, "Scott Wedgewood"),
    (28, "Carter Hart"),
    (29, "John Gibson"),
    (30, "Daniil Tarasov"),
    (31, "Frederik Andersen"),
    (32, "Joey Daccord"),
    (33, "Darcy Kuemper"),
    (34, "Sebastian Cossa"),
    (35, "Jacob Fowler"),
    (36, "Anton Forsberg"),
    (37, "Sergey Murashov"),
    (38, "Arturs Silovs"),
    (39, "Pyotr Kochetkov"),
    (40, "Adin Hill"),
    (41, "Stuart Skinner"),
    (42, "Thatcher Demko"),
    (43, "Jordan Binnington"),
    (44, "Alex Lyon"),
    (45, "Devin Cooley"),
    (46, "Tristan Jarry"),
    (47, "Joshua Ravensbergen"),
    (48, "Samuel Ersson"),
    (49, "Casey DeSmith"),
    (50, "Philipp Grubauer"),
    (51, "Joseph Woll"),
    (52, "Dennis Hildeby"),
    (53, "Justus Annunen"),
    (54, "Anthony Stolarz"),
    (55, "David Rittich"),
    (56, "Elvis Merzlikins"),
]


def normalize(name):
    name = unicodedata.normalize("NFKD", name)
    name = name.encode("ascii", "ignore").decode("ascii")
    name = name.lower()
    name = re.sub(r"\b(jr|sr|ii|iii|iv|v)\b\.?", "", name)
    name = re.sub(r"[^a-z\s]", "", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name


with open(MASTER_PATH, newline="") as f:
    reader = csv.DictReader(f)
    fieldnames = list(reader.fieldnames)
    rows = list(reader)

if SOURCE_COL not in fieldnames:
    fieldnames.insert(fieldnames.index("Average Rank"), SOURCE_COL)
    for row in rows:
        row[SOURCE_COL] = ""

lookup = {normalize(row["Player"]): row for row in rows}

new_players = []
for rank, name in GOALIE_DATA:
    key = normalize(name)
    if key in lookup:
        lookup[key][SOURCE_COL] = rank
    else:
        new_row = {fn: "" for fn in fieldnames}
        new_row["Player"] = name
        new_row["Position"] = "G"
        new_row["Age"] = ""
        new_row[SOURCE_COL] = rank
        new_row["Average Rank"] = ""
        new_row["Rank Variance"] = ""
        new_players.append(new_row)
        rows.append(new_row)
        lookup[key] = new_row

with open(MASTER_PATH, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Merged {len(GOALIE_DATA)} Dynasty Puck goalies.")
print(f"  Matched: {len(GOALIE_DATA) - len(new_players)}")
print(f"  New players added: {len(new_players)}")
if new_players:
    for p in new_players:
        print(f"    + {p['Player']}")

subprocess.run(["python3", os.path.join(os.path.dirname(__file__), "recalculate.py"), MASTER_PATH])
