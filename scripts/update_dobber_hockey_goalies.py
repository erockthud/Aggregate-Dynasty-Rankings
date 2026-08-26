#!/usr/bin/env python3
"""
Update Dobber hockey goalie rankings from Mar 2026 to Aug 2026.
Renames the column and replaces all values.
Run recalculate.py afterward.
"""

import csv
import os
import re
import subprocess
import unicodedata

MASTER_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "hockey", "hockey_goalies_master.csv"))
OLD_COL = "Dobber (Mar 2026)"
NEW_COL = "Dobber (Aug 2026)"

DOBBER_DATA = [
    (1, "Andrei Vasilevskiy"),
    (2, "Logan Thompson"),
    (3, "Igor Shesterkin"),
    (4, "Jake Oettinger"),
    (5, "Jeremy Swayman"),
    (6, "Connor Hellebuyck"),
    (7, "Karel Vejmelka"),
    (8, "Ilya Sorokin"),
    (9, "Lukas Dostal"),
    (10, "Carter Hart"),
    (11, "Mackenzie Blackwood"),
    (12, "Spencer Knight"),
    (13, "Linus Ullmark"),
    (14, "Daniel Vladar"),
    (15, "Brandon Bussi"),
    (16, "Jesper Wallstedt"),
    (17, "Jakub Dobes"),
    (18, "Filip Gustavsson"),
    (19, "Dustin Wolf"),
    (20, "Jacob Fowler"),
    (21, "Yaroslav Askarov"),
    (22, "Juuse Saros"),
    (23, "Ukko-Pekka Luukkonen"),
    (24, "John Gibson"),
    (25, "Jet Greaves"),
    (26, "Devon Levi"),
    (27, "Scott Wedgewood"),
    (28, "Joey Daccord"),
    (29, "Arturs Silovs"),
    (30, "Joel Hofer"),
    (31, "Sergei Bobrovsky"),
    (32, "Jacob Markstrom"),
    (33, "Alex Lyon"),
    (34, "Joseph Woll"),
    (35, "Daniil Tarasov"),
    (36, "Darcy Kuemper"),
    (37, "Frederik Andersen"),
    (38, "Nico Daws"),
    (39, "Sergey Murashov"),
    (40, "Sebastian Cossa"),
    (41, "Stuart Skinner"),
    (42, "Devin Cooley"),
    (43, "Akira Schmid"),
    (44, "Jordan Binnington"),
    (45, "Anton Forsberg"),
    (46, "Colten Ellis"),
    (47, "Jake Allen"),
    (48, "Tristan Jarry"),
    (49, "Alex Nedeljkovic"),
    (50, "Pyotr Kochetkov"),
    (51, "Dylan Garand"),
    (52, "Kevin Lankinen"),
    (53, "Thatcher Demko"),
    (54, "Ville Husso"),
    (55, "Anthony Stolarz"),
    (56, "Elvis Merzlikins"),
    (57, "Adin Hill"),
    (58, "Sam Montembeault"),
    (59, "Joonas Korpisalo"),
    (60, "Philipp Grubauer"),
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

if OLD_COL in fieldnames:
    fieldnames[fieldnames.index(OLD_COL)] = NEW_COL
    for row in rows:
        row[NEW_COL] = row.pop(OLD_COL, "")

for row in rows:
    row[NEW_COL] = ""

lookup = {normalize(row["Player"]): row for row in rows}

new_players = []
unmatched = []
for rank, name in DOBBER_DATA:
    key = normalize(name)
    if key in lookup:
        lookup[key][NEW_COL] = rank
    else:
        unmatched.append((rank, name))
        new_row = {fn: "" for fn in fieldnames}
        new_row["Player"] = name
        new_row["Position"] = "G"
        new_row["Age"] = ""
        new_row[NEW_COL] = rank
        new_row["Average Rank"] = ""
        new_row["Rank Variance"] = ""
        new_players.append(new_row)
        rows.append(new_row)
        lookup[key] = new_row

with open(MASTER_PATH, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Updated {len(DOBBER_DATA)} Dobber goalie rankings ({OLD_COL} -> {NEW_COL}).")
print(f"  Matched: {len(DOBBER_DATA) - len(new_players)}")
print(f"  New players added: {len(new_players)}")
if new_players:
    for rank, name in unmatched:
        print(f"    + [{rank}] {name}")

subprocess.run(["python3", os.path.join(os.path.dirname(__file__), "recalculate.py"), MASTER_PATH])
