#!/usr/bin/env python3
"""
Replace FantasyCalc (Crowdsourced, 2026-03) with Dynatyze (Crowdsourced, 2026-05)
in football_rankings_master.csv. Renames the column header and updates all ranks.
Run recalculate.py afterward.
"""

import csv
import os
import re
import subprocess
import unicodedata

MASTER_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "football", "football_rankings_master.csv"))
OLD_COL = "FantasyCalc (Crowdsourced, 2026-03)"
NEW_COL = "Dynatyze (Crowdsourced, 2026-05)"

# Dynatyze uses short names for some players — map to canonical master names
NAME_MAP = {
    "chig okonkwo": "Chigoziem Okonkwo",
}

# (rank, name, position, age)
PLAYER_DATA = [
    (1,   "Puka Nacua",               "WR", 24),
    (2,   "Bijan Robinson",           "RB", 24),
    (3,   "Jahmyr Gibbs",             "RB", 24),
    (4,   "Amon-Ra St. Brown",        "WR", 26),
    (5,   "Josh Allen",               "QB", 29),
    (6,   "James Cook",               "RB", 26),
    (7,   "Lamar Jackson",            "QB", 29),
    (8,   "Jonathan Taylor",          "RB", 27),
    (9,   "CeeDee Lamb",              "WR", 27),
    (10,  "Jalen Hurts",              "QB", 27),
    (11,  "Ja'Marr Chase",            "WR", 26),
    (12,  "Justin Jefferson",         "WR", 26),
    (13,  "Jayden Daniels",           "QB", 25),
    (14,  "Patrick Mahomes",          "QB", 30),
    (15,  "Christian McCaffrey",      "RB", 29),
    (16,  "Jaxon Smith-Njigba",       "WR", 24),
    (17,  "Malik Nabers",             "WR", 22),
    (18,  "Bo Nix",                   "QB", 26),
    (19,  "Drake Maye",               "QB", 23),
    (20,  "Breece Hall",              "RB", 24),
    (21,  "Kyren Williams",           "RB", 25),
    (22,  "Brock Bowers",             "TE", 23),
    (23,  "Jaxson Dart",              "QB", 22),
    (24,  "Trey McBride",             "TE", 26),
    (25,  "Javonte Williams",         "RB", 26),
    (26,  "Saquon Barkley",           "RB", 29),
    (27,  "Joe Burrow",               "QB", 29),
    (28,  "Josh Jacobs",              "RB", 28),
    (29,  "Drake London",             "WR", 24),
    (30,  "Nico Collins",             "WR", 27),
    (31,  "Derrick Henry",            "RB", 32),
    (32,  "Caleb Williams",           "QB", 24),
    (33,  "Kenneth Walker III",       "RB", 25),
    (34,  "Rome Odunze",              "WR", 23),
    (35,  "Sam LaPorta",              "TE", 25),
    (36,  "Dak Prescott",             "QB", 32),
    (37,  "Omarion Hampton",          "RB", 23),
    (38,  "A.J. Brown",               "WR", 28),
    (39,  "Tee Higgins",              "WR", 27),
    (40,  "Garrett Wilson",           "WR", 25),
    (41,  "Ashton Jeanty",            "RB", 22),
    (42,  "Tyler Warren",             "TE", 23),
    (43,  "Justin Herbert",           "QB", 28),
    (44,  "Colston Loveland",         "TE", 22),
    (45,  "De'Von Achane",            "RB", 24),
    (46,  "Trevor Lawrence",          "QB", 26),
    (47,  "Travis Etienne",           "RB", 27),
    (48,  "Quinshon Judkins",         "RB", 22),
    (49,  "George Pickens",           "WR", 25),
    (50,  "Ladd McConkey",            "WR", 24),
    (51,  "Brock Purdy",              "QB", 26),
    (52,  "Tucker Kraft",             "TE", 25),
    (53,  "Cam Skattebo",             "RB", 24),
    (54,  "Jordan Love",              "QB", 27),
    (55,  "Jeremiyah Love",           "RB", 20),
    (56,  "Tetairoa McMillan",        "WR", 23),
    (57,  "Kyle Pitts",               "TE", 25),
    (58,  "C.J. Stroud",              "QB", 24),
    (59,  "Brian Thomas Jr.",         "WR", 23),
    (60,  "Marvin Harrison Jr.",      "WR", 23),
    (61,  "Harold Fannin Jr.",        "TE", 21),
    (62,  "George Kittle",            "TE", 32),
    (63,  "Baker Mayfield",           "QB", 31),
    (64,  "Chase Brown",              "RB", 26),
    (65,  "Tyler Shough",             "QB", 26),
    (66,  "Jake Ferguson",            "TE", 27),
    (67,  "Fernando Mendoza",         "QB", 22),
    (68,  "T.J. Hockenson",           "TE", 28),
    (69,  "Kyler Murray",             "QB", 28),
    (70,  "Zay Flowers",              "WR", 25),
    (71,  "DeVonta Smith",            "WR", 27),
    (72,  "Jaylen Waddle",            "WR", 27),
    (73,  "Chuba Hubbard",            "RB", 26),
    (74,  "Chris Olave",              "WR", 25),
    (75,  "Bryce Young",              "QB", 24),
    (76,  "Travis Kelce",             "TE", 36),
    (77,  "TreVeyon Henderson",       "RB", 23),
    (78,  "DK Metcalf",               "WR", 28),
    (79,  "Dalton Schultz",           "TE", 29),
    (80,  "Cam Ward",                 "QB", 23),
    (81,  "Chig Okonkwo",             "TE", 26),
    (82,  "Jared Goff",               "QB", 31),
    (83,  "Bucky Irving",             "RB", 23),
    (84,  "Matthew Stafford",         "QB", 38),
    (85,  "Emeka Egbuka",             "WR", 23),
    (86,  "Brenton Strange",          "TE", 25),
    (87,  "Tony Pollard",             "RB", 29),
    (88,  "Terry McLaurin",           "WR", 30),
    (89,  "Davante Adams",            "WR", 33),
    (90,  "Michael Pittman",          "WR", 28),
    (91,  "Sam Darnold",              "QB", 28),
    (92,  "Makai Lemon",              "WR", 21),
    (93,  "Mark Andrews",             "TE", 30),
    (94,  "Daniel Jones",             "QB", 28),
    (95,  "D'Andre Swift",            "RB", 27),
    (96,  "Pat Freiermuth",           "TE", 27),
    (97,  "Zach Charbonnet",          "RB", 25),
    (98,  "Xavier Worthy",            "WR", 23),
    (99,  "Courtland Sutton",         "WR", 30),
    (100, "Tua Tagovailoa",           "QB", 28),
    (101, "Rashee Rice",              "WR", 26),
    (102, "Luther Burden III",        "WR", 22),
    (103, "Jaylen Warren",            "RB", 27),
    (104, "Brandon Aiyuk",            "WR", 28),
    (105, "Khalil Shakir",            "WR", 26),
    (106, "Jayden Reed",              "WR", 26),
    (107, "RJ Harvey",                "RB", 25),
    (108, "Bhayshul Tuten",           "RB", 24),
    (109, "Rhamondre Stevenson",      "RB", 28),
    (110, "Shedeur Sanders",          "QB", 24),
    (111, "Dalton Kincaid",           "TE", 26),
    (112, "DJ Moore",                 "WR", 29),
    (113, "Josh Downs",               "WR", 24),
    (114, "Michael Penix Jr.",        "QB", 25),
    (115, "J.J. McCarthy",            "QB", 23),
    (116, "Aaron Jones",              "RB", 31),
    (117, "Wan'Dale Robinson",        "WR", 25),
    (118, "Michael Wilson",           "WR", 26),
    (119, "Jameson Williams",         "WR", 25),
    (120, "Kenyon Sadiq",             "TE", 21),
    (121, "David Njoku",              "TE", 29),
    (122, "Ricky Pearsall",           "WR", 25),
    (123, "Jordan Addison",           "WR", 24),
    (124, "Mike Evans",               "WR", 32),
    (125, "Dallas Goedert",           "TE", 31),
    (126, "Isaiah Likely",            "TE", 26),
    (127, "Jacory Croskey-Merritt",   "RB", 25),
    (128, "Isiah Pacheco",            "RB", 27),
    (129, "Blake Corum",              "RB", 25),
    (130, "Kyle Monangai",            "RB", 23),
    (131, "Romeo Doubs",              "WR", 26),
    (132, "Kenneth Gainwell",         "RB", 27),
    (133, "Gunnar Helm",              "TE", 23),
    (134, "Ty Simpson",               "QB", 23),
    (135, "Drew Allar",               "QB", 0),
    (136, "David Montgomery",         "RB", 28),
    (137, "AJ Barner",                "TE", 24),
    (138, "Cade Otton",               "TE", 27),
    (139, "Ja'Tavion Sanders",        "TE", 23),
    (140, "Tyler Allgeier",           "RB", 26),
    (141, "Matthew Golden",           "WR", 22),
    (142, "Woody Marks",              "RB", 25),
    (143, "Jordyn Tyson",             "WR", 21),
    (144, "Oronde Gadsden II",        "TE", 22),
    (145, "Carnell Tate",             "WR", 21),
    (146, "Malik Willis",             "QB", 26),
    (147, "Deebo Samuel Sr.",         "WR", 30),
    (148, "Jerry Jeudy",              "WR", 27),
    (149, "Zach Ertz",                "TE", 35),
    (150, "Denzel Boston",            "WR", 22),
    (151, "J.K. Dobbins",             "RB", 27),
    (152, "Alvin Kamara",             "RB", 30),
    (153, "James Conner",             "RB", 30),
    (154, "Brian Robinson",           "RB", 27),
    (155, "Rachaad White",            "RB", 27),
    (156, "Brashard Smith",           "RB", 23),
    (157, "Nicholas Singleton",       "RB", 22),
    (158, "Braelon Allen",            "RB", 22),
    (159, "Stefon Diggs",             "WR", 32),
    (160, "Alec Pierce",              "WR", 26),
    (161, "Tyler Higbee",             "TE", 33),
    (162, "Aaron Rodgers",            "QB", 42),
    (163, "Russell Wilson",           "QB", 37),
    (164, "Kirk Cousins",             "QB", 37),
    (165, "Quinn Ewers",              "QB", 23),
    (166, "Tyrone Tracy Jr.",         "RB", 26),
    (167, "Dylan Sampson",            "RB", 21),
    (168, "Sean Tucker",              "RB", 24),
    (169, "Jadarian Price",           "RB", 22),
    (170, "Calvin Ridley",            "WR", 31),
    (171, "Jakobi Meyers",            "WR", 29),
    (172, "Jonah Coleman",            "RB", 23),
    (173, "Jordan Mason",             "RB", 26),
    (174, "Hunter Henry",             "TE", 31),
    (175, "Juwan Johnson",            "TE", 29),
    (176, "Parker Washington",        "WR", 24),
    (177, "Cole Kmet",                "TE", 27),
    (178, "Pat Bryant",               "WR", 23),
    (179, "Theo Johnson",             "TE", 25),
    (180, "Tyjae Spears",             "RB", 24),
    (181, "Rashid Shaheed",           "WR", 27),
    (182, "Evan Engram",              "TE", 31),
    (183, "Nick Chubb",               "RB", 30),
    (184, "Jauan Jennings",           "WR", 28),
    (185, "Jayden Higgins",           "WR", 23),
    (186, "Jalen Coker",              "WR", 24),
    (187, "Jerome Ford",              "RB", 26),
    (188, "Tank Dell",                "WR", 26),
    (189, "Joe Mixon",                "RB", 29),
    (190, "KC Concepcion",            "WR", 22),
    (191, "Najee Harris",             "RB", 28),
    (192, "Jake Tonges",              "TE", 26),
    (193, "Mike Gesicki",             "TE", 30),
    (194, "Anthony Richardson",       "QB", 23),
    (196, "Justin Fields",            "QB", 27),
    (197, "Luke Musgrave",            "TE", 25),
    (198, "Terrance Ferguson",        "TE", 23),
    (199, "Austin Ekeler",            "RB", 30),
    (200, "Chris Godwin Jr.",         "WR", 30),
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

# Rename the column in-place
if OLD_COL in fieldnames:
    fieldnames[fieldnames.index(OLD_COL)] = NEW_COL
    for row in rows:
        row[NEW_COL] = row.pop(OLD_COL, "")
elif NEW_COL not in fieldnames:
    fieldnames.insert(fieldnames.index("Average Rank"), NEW_COL)

# Clear existing values so only Dynatyze data remains
for row in rows:
    row[NEW_COL] = ""

lookup = {normalize(row["Player"]): row for row in rows}

new_players = []
for rank, name, pos, age in PLAYER_DATA:
    key = normalize(name)
    canonical = NAME_MAP.get(key, name)
    canon_key = normalize(canonical)

    row = lookup.get(canon_key) or lookup.get(key)
    if row:
        row[NEW_COL] = rank
    else:
        new_row = {fn: "" for fn in fieldnames}
        new_row["Player"] = canonical
        new_row["Position"] = pos
        new_row["Age"] = "" if age == 0 else str(age)
        new_row[NEW_COL] = rank
        new_players.append(new_row)
        rows.append(new_row)
        lookup[canon_key] = new_row

with open(MASTER_PATH, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Merged {len(PLAYER_DATA)} Dynatyze players.")
print(f"  Matched: {len(PLAYER_DATA) - len(new_players)}")
print(f"  New players added: {len(new_players)}")
if new_players:
    for p in new_players:
        print(f"    + {p['Player']} ({p['Position']})")

subprocess.run(["python3", os.path.join(os.path.dirname(__file__), "recalculate.py"), MASTER_PATH])
