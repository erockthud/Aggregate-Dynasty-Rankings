#!/usr/bin/env python3
"""
Create hockey/hockey_goalies_master.csv from Dobber goalie rankings.
Run recalculate.py afterward to compute Average Rank / Rank Variance.
"""

import csv
import os

# (rank, name, team)
DOBBER_DATA = [
    (1, "Andrei Vasilevskiy", "TBL"),
    (2, "Igor Shesterkin", "NYR"),
    (3, "Connor Hellebuyck", "WPG"),
    (4, "Jake Oettinger", "DAL"),
    (5, "Filip Gustavsson", "MIN"),
    (6, "Logan Thompson", "WAS"),
    (7, "Ilya Sorokin", "NYI"),
    (8, "Mackenzie Blackwood", "COL"),
    (9, "Lukas Dostal", "ANA"),
    (10, "Spencer Knight", "CHI"),
    (11, "Sergei Bobrovsky", "FLA"),
    (12, "Karel Vejmelka", "UTA"),
    (13, "Jeremy Swayman", "BOS"),
    (14, "Brandon Bussi", "CAR"),
    (15, "Joey Daccord", "SEA"),
    (16, "Dustin Wolf", "CGY"),
    (17, "Juuse Saros", "NSH"),
    (18, "Yaroslav Askarov", "SJS"),
    (19, "Linus Ullmark", "OTT"),
    (20, "Tristan Jarry", "EDM"),
    (21, "John Gibson", "DET"),
    (22, "Jacob Markstrom", "NJD"),
    (23, "Darcy Kuemper", "LAK"),
    (24, "Dan Vladar", "PHI"),
    (25, "Jesper Wallstedt", "MIN"),
    (26, "Jet Greaves", "CBJ"),
    (27, "Jakub Dobes", "MON"),
    (28, "Arturs Silovs", "PIT"),
    (29, "Joseph Woll", "TOR"),
    (30, "Ukko-Pekka Luukkonen", "BUF"),
    (31, "Stuart Skinner", "PIT"),
    (32, "Jordan Binnington", "STL"),
    (33, "Sam Montembeault", "MON"),
    (34, "Alex Lyon", "BUF"),
    (35, "Kevin Lankinen", "VAN"),
    (36, "Adin Hill", "VGK"),
    (37, "Anthony Stolarz", "TOR"),
    (38, "Scott Wedgewood", "COL"),
    (39, "Jacob Fowler", "MON"),
    (40, "Connor Ingram", "EDM"),
    (41, "Leevi Merilainen", "OTT"),
    (42, "Joel Hofer", "STL"),
    (43, "Elvis Merzlikins", "CBJ"),
    (44, "Carter Hart", "VGK"),
    (45, "Devon Levi", "BUF"),
    (46, "Akira Schmid", "VGK"),
    (47, "Alex Nedeljkovic", "SJS"),
    (48, "Sebastian Cossa", "DET"),
    (49, "David Rittich", "NYI"),
    (50, "Pyotr Kochetkov", "CAR"),
    (51, "Eric Comrie", "WPG"),
    (52, "Colten Ellis", "BUF"),
    (53, "Jake Allen", "NJD"),
    (54, "Thatcher Demko", "VAN"),
    (55, "Ville Husso", "ANA"),
    (56, "Sergey Murashov", "PIT"),
    (57, "Joonas Korpisalo", "BOS"),
    (58, "Philipp Grubauer", "SEA"),
    (59, "Dennis Hildeby", "TOR"),
    (60, "Frederik Andersen", "CAR"),
]

SOURCE_COL = "Dobber (Mar 2026)"
FIELDNAMES = ["Player", "Position", "Age", SOURCE_COL, "Average Rank", "Rank Variance"]

out_path = os.path.join(os.path.dirname(__file__), "..", "hockey", "hockey_goalies_master.csv")
out_path = os.path.normpath(out_path)

rows = []
for rank, name, team in DOBBER_DATA:
    rows.append({
        "Player": name,
        "Position": "G",
        "Age": "",
        SOURCE_COL: rank,
        "Average Rank": "",
        "Rank Variance": "",
    })

with open(out_path, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote {len(rows)} goalies to {out_path}")
