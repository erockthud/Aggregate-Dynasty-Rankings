#!/usr/bin/env python3
"""
Merge Hashtag Hockey (Mar 2026) goalie rankings into hockey_goalies_master.csv.
Run recalculate.py afterward.
"""

import csv
import os
import re
import subprocess
import unicodedata

MASTER_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "hockey", "hockey_goalies_master.csv"))
SOURCE_COL = "Hashtag Hockey (Mar 2026)"

HASHTAG_DATA = [
    (1, "Connor Hellebuyck"),
    (2, "Jake Oettinger"),
    (3, "Andrei Vasilevskiy"),
    (4, "Igor Shesterkin"),
    (5, "Ilya Sorokin"),
    (6, "Jacob Markstrom"),
    (7, "Logan Thompson"),
    (8, "Juuse Saros"),
    (9, "Darcy Kuemper"),
    (10, "Dustin Wolf"),
    (11, "Mackenzie Blackwood"),
    (12, "Thatcher Demko"),
    (13, "Linus Ullmark"),
    (14, "Filip Gustavsson"),
    (15, "Joey Daccord"),
    (16, "Sergei Bobrovsky"),
    (17, "Jeremy Swayman"),
    (18, "Karel Vejmelka"),
    (19, "Jordan Binnington"),
    (20, "Pyotr Kochetkov"),
    (21, "Ukko-Pekka Luukkonen"),
    (22, "Lukas Dostal"),
    (23, "Joseph Woll"),
    (24, "Adin Hill"),
    (25, "Stuart Skinner"),
    (26, "John Gibson"),
    (27, "Kevin Lankinen"),
    (28, "Yaroslav Askarov"),
    (29, "Jesper Wallstedt"),
    (30, "Sam Montembeault"),
    (31, "Connor Ingram"),
    (32, "Devon Levi"),
    (33, "Cam Talbot"),
    (34, "Elvis Merzlikins"),
    (35, "Anthony Stolarz"),
    (36, "Frederik Andersen"),
    (37, "Samuel Ersson"),
    (38, "Joel Hofer"),
    (39, "Charlie Lindgren"),
    (40, "Ivan Fedotov"),
    (41, "Casey DeSmith"),
    (42, "Scott Wedgewood"),
    (43, "Jake Allen"),
    (44, "Vitek Vanecek"),
    (45, "Alex Lyon"),
    (46, "Joonas Korpisalo"),
    (47, "Anton Forsberg"),
    (48, "Petr Mrazek"),
    (49, "Alexandar Georgiev"),
    (50, "Tristan Jarry"),
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
for rank, name in HASHTAG_DATA:
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

print(f"Merged {len(HASHTAG_DATA)} Hashtag Hockey goalies.")
print(f"  Matched: {len(HASHTAG_DATA) - len(new_players)}")
print(f"  New players added: {len(new_players)}")
if new_players:
    for p in new_players:
        print(f"    + {p['Player']}")

subprocess.run(["python3", os.path.join(os.path.dirname(__file__), "recalculate.py"), MASTER_PATH])
