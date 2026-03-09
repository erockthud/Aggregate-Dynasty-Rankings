#!/usr/bin/env python3
"""
Merge RankKing (Mar 2026) goalie rankings into hockey_goalies_master.csv.
Run recalculate.py afterward.
"""

import csv
import os
import re
import subprocess
import unicodedata

MASTER_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "hockey", "hockey_goalies_master.csv"))
SOURCE_COL = "RankKing (Mar 2026)"

RANKKING_DATA = [
    (1, "Andrei Vasilevskiy"),
    (2, "Connor Hellebuyck"),
    (3, "Igor Shesterkin"),
    (4, "Jake Oettinger"),
    (5, "Logan Thompson"),
    (6, "Jesper Wallstedt"),
    (7, "Ilya Sorokin"),
    (8, "Sergei Bobrovsky"),
    (9, "Filip Gustavsson"),
    (10, "Mackenzie Blackwood"),
    (11, "Dustin Wolf"),
    (12, "Jeremy Swayman"),
    (13, "Juuse Saros"),
    (14, "Joseph Woll"),
    (15, "Spencer Knight"),
    (16, "Lukas Dostal"),
    (17, "John Gibson"),
    (18, "Yaroslav Askarov"),
    (19, "Darcy Kuemper"),
    (20, "Karel Vejmelka"),
    (21, "Joey Daccord"),
    (22, "Jordan Binnington"),
    (23, "Ukko-Pekka Luukkonen"),
    (24, "Linus Ullmark"),
    (25, "Jacob Markstrom"),
    (26, "Thatcher Demko"),
    (27, "Tristan Jarry"),
    (28, "Scott Wedgewood"),
    (29, "Samuel Montembeault"),
    (30, "Jet Greaves"),
    (31, "Dan Vladar"),
    (32, "Anthony Stolarz"),
    (33, "Jake Allen"),
    (34, "Adin Hill"),
    (35, "Stuart Skinner"),
    (36, "Pyotr Kochetkov"),
    (37, "Jakub Dobes"),
    (38, "Joel Hofer"),
    (39, "Carter Hart"),
    (40, "Alex Lyon"),
]

# Map source name variants to canonical master names
NAME_MAP = {
    "samuel montembeault": "Sam Montembeault",
}


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
for rank, name in RANKKING_DATA:
    key = normalize(name)
    canonical = NAME_MAP.get(key, name)
    canonical_key = normalize(canonical)
    if canonical_key in lookup:
        lookup[canonical_key][SOURCE_COL] = rank
    elif key in lookup:
        lookup[key][SOURCE_COL] = rank
    else:
        new_row = {fn: "" for fn in fieldnames}
        new_row["Player"] = canonical
        new_row["Position"] = "G"
        new_row["Age"] = ""
        new_row[SOURCE_COL] = rank
        new_row["Average Rank"] = ""
        new_row["Rank Variance"] = ""
        new_players.append(new_row)
        rows.append(new_row)
        lookup[canonical_key] = new_row

with open(MASTER_PATH, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Merged {len(RANKKING_DATA)} RankKing goalies.")
print(f"  Matched: {len(RANKKING_DATA) - len(new_players)}")
print(f"  New players added: {len(new_players)}")
if new_players:
    for p in new_players:
        print(f"    + {p['Player']}")

subprocess.run(["python3", os.path.join(os.path.dirname(__file__), "recalculate.py"), MASTER_PATH])
