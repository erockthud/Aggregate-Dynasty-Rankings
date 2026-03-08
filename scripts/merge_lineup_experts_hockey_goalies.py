#!/usr/bin/env python3
"""
Merge Lineup Experts (Oct 2025) goalie rankings into hockey_goalies_master.csv.
Goalies are ranked 1-34 by their position among goalies only (not overall rank).
Run recalculate.py afterward.
"""

import csv
import os
import re
import subprocess
import unicodedata

MASTER_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "hockey", "hockey_goalies_master.csv"))
SOURCE_COL = "Lineup Experts (Oct 2025)"

# (goalie_rank, name)  — ranked 1-34 by order of appearance in Lineup Experts combined list
# Original overall ranks (among all players): Oettinger=15, Hellebuyck=18, Vasilevskiy=35, etc.
GOALIE_DATA = [
    (1,  "Jake Oettinger"),
    (2,  "Connor Hellebuyck"),
    (3,  "Andrei Vasilevskiy"),
    (4,  "Dustin Wolf"),
    (5,  "Igor Shesterkin"),
    (6,  "Filip Gustavsson"),
    (7,  "Mackenzie Blackwood"),
    (8,  "Jeremy Swayman"),
    (9,  "Ilya Sorokin"),
    (10, "Logan Thompson"),
    (11, "Lukas Dostal"),
    (12, "Linus Ullmark"),
    (13, "Juuse Saros"),
    (14, "Sergei Bobrovsky"),
    (15, "Darcy Kuemper"),
    (16, "Stuart Skinner"),
    (17, "Sam Montembeault"),
    (18, "Adin Hill"),
    (19, "Anthony Stolarz"),
    (20, "Spencer Knight"),
    (21, "Jordan Binnington"),
    (22, "Jacob Markstrom"),
    (23, "Thatcher Demko"),
    (24, "Yaroslav Askarov"),
    (25, "Karel Vejmelka"),
    (26, "Joey Daccord"),
    (27, "Samuel Ersson"),
    (28, "Frederik Andersen"),
    (29, "Joseph Woll"),
    (30, "Ukko-Pekka Luukkonen"),
    (31, "Elvis Merzlikins"),
    (32, "Pyotr Kochetkov"),
    (33, "John Gibson"),
    (34, "Jet Greaves"),
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

print(f"Merged {len(GOALIE_DATA)} Lineup Experts goalies.")
print(f"  Matched: {len(GOALIE_DATA) - len(new_players)}")
print(f"  New players added: {len(new_players)}")
if new_players:
    for p in new_players:
        print(f"    + {p['Player']}")

subprocess.run(["python3", os.path.join(os.path.dirname(__file__), "recalculate.py"), MASTER_PATH])
