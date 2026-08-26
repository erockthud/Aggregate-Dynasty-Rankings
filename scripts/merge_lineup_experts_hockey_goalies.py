#!/usr/bin/env python3
"""
Merge Lineup Experts (Aug 2026) goalie rankings into hockey_goalies_master.csv.
Goalies are ranked 1-N by their position among goalies only (not overall rank).
Run recalculate.py afterward.
"""

import csv
import os
import re
import subprocess
import unicodedata

MASTER_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "hockey", "hockey_goalies_master.csv"))
OLD_SOURCE_COL = "Lineup Experts (Oct 2025)"
SOURCE_COL = "Lineup Experts (Aug 2026)"

# (goalie_rank, name) — ranked 1-N by order of appearance in Lineup Experts combined list
GOALIE_DATA = [
    (1, "Andrei Vasilevskiy"),
    (2, "Jake Oettinger"),
    (3, "Jet Greaves"),
    (4, "Logan Thompson"),
    (5, "Igor Shesterkin"),
    (6, "Karel Vejmelka"),
    (7, "Connor Hellebuyck"),
    (8, "Jeremy Swayman"),
    (9, "Spencer Knight"),
    (10, "Ilya Sorokin"),
    (11, "Dustin Wolf"),
    (12, "Lukas Dostal"),
    (13, "Joel Hofer"),
    (14, "Brandon Bussi"),
    (15, "Juuse Saros"),
    (16, "John Gibson"),
    (17, "Joey Daccord"),
    (18, "Carter Hart"),
    (19, "Ukko-Pekka Luukkonen"),
    (20, "Jesper Wallstedt"),
    (21, "Scott Wedgewood"),
    (22, "Daniel Vladar"),
    (23, "Yaroslav Askarov"),
    (24, "Linus Ullmark"),
    (25, "Darcy Kuemper"),
    (26, "Jake Allen"),
    (27, "Jacob Markstrom"),
    (28, "Sergei Bobrovsky"),
    (29, "Anthony Stolarz"),
    (30, "Mackenzie Blackwood"),
    (31, "Tristan Jarry"),
    (32, "Thatcher Demko"),
    (33, "Filip Gustavsson"),
    (34, "Jakub Dobes"),
    (35, "Arturs Silovs"),
    (36, "Pyotr Kochetkov"),
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

if OLD_SOURCE_COL in fieldnames:
    fieldnames = [SOURCE_COL if fn == OLD_SOURCE_COL else fn for fn in fieldnames]
    for row in rows:
        row[SOURCE_COL] = ""
        if OLD_SOURCE_COL in row:
            del row[OLD_SOURCE_COL]
elif SOURCE_COL not in fieldnames:
    fieldnames.insert(fieldnames.index("Average Rank"), SOURCE_COL)
    for row in rows:
        row[SOURCE_COL] = ""
else:
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

print(f"Merged {len(GOALIE_DATA)} Lineup Experts goalies.")
print(f"  Matched: {len(GOALIE_DATA) - len(new_players)}")
print(f"  New players added: {len(new_players)}")
if new_players:
    for p in new_players:
        print(f"    + {p['Player']}")

subprocess.run(["python3", os.path.join(os.path.dirname(__file__), "recalculate.py"), MASTER_PATH])
