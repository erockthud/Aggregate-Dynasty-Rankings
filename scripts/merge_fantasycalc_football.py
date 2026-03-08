#!/usr/bin/env python3
"""
Merge FantasyCalc (Mar 2026) football rankings into football_rankings_master.csv.
Also backfills Age for matched players where Age is currently blank.
Run recalculate.py afterward.
"""

import csv
import os
import re
import subprocess
import unicodedata

MASTER_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "football", "football_rankings_master.csv"))
SOURCE_COL = "FantasyCalc (Crowdsourced, 2026-03)"

# (rank, name, position, age_str)  — age_str is '' for rookies marked 'R'
PLAYER_DATA = [
    (1,   "Bijan Robinson",         "RB", "24.1"),
    (2,   "Josh Allen",             "QB", "29.8"),
    (3,   "Ja'Marr Chase",          "WR", "26.0"),
    (4,   "Jaxon Smith-Njigba",     "WR", "24.0"),
    (5,   "Puka Nacua",             "WR", "24.7"),
    (6,   "Jahmyr Gibbs",           "RB", "23.9"),
    (7,   "Drake Maye",             "QB", "23.5"),
    (8,   "Jayden Daniels",         "QB", "25.2"),
    (9,   "Lamar Jackson",          "QB", "29.1"),
    (10,  "Brock Bowers",           "TE", "23.2"),
    (11,  "Malik Nabers",           "WR", "22.6"),
    (12,  "Amon-Ra St. Brown",      "WR", "26.3"),
    (13,  "Justin Jefferson",       "WR", "26.7"),
    (14,  "Caleb Williams",         "QB", "24.3"),
    (15,  "Trey McBride",           "TE", "26.2"),
    (16,  "Joe Burrow",             "QB", "29.2"),
    (17,  "CeeDee Lamb",            "WR", "26.9"),
    (18,  "Ashton Jeanty",          "RB", "22.2"),
    (19,  "Jeremiyah Love",         "RB", ""),
    (20,  "Justin Herbert",         "QB", "27.9"),
    (21,  "De'Von Achane",          "RB", "24.4"),
    (22,  "Drake London",           "WR", "24.6"),
    (23,  "Omarion Hampton",        "RB", "22.9"),
    (24,  "Patrick Mahomes",        "QB", "30.4"),
    (25,  "Jalen Hurts",            "QB", "27.5"),
    (26,  "Jaxson Dart",            "QB", "22.8"),
    (27,  "Jonathan Taylor",        "RB", "27.1"),
    (28,  "Tetairoa McMillan",      "WR", "22.9"),
    (29,  "James Cook",             "RB", "26.4"),
    (30,  "Bo Nix",                 "QB", "26.0"),
    (31,  "Colston Loveland",       "TE", "21.9"),
    (32,  "Brock Purdy",            "QB", "26.1"),
    (33,  "Trevor Lawrence",        "QB", "26.4"),
    (34,  "George Pickens",         "WR", "25.0"),
    (35,  "Makai Lemon",            "WR", ""),
    (36,  "Nico Collins",           "WR", "26.9"),
    (37,  "Carnell Tate",           "WR", ""),
    (38,  "Garrett Wilson",         "WR", "25.6"),
    (39,  "Emeka Egbuka",           "WR", "23.3"),
    (40,  "Tyler Warren",           "TE", "23.7"),
    (41,  "Jordan Love",            "QB", "27.3"),
    (42,  "Fernando Mendoza",       "QB", ""),
    (43,  "Bucky Irving",           "RB", "23.5"),
    (44,  "Dak Prescott",           "QB", "32.6"),
    (45,  "Christian McCaffrey",    "RB", "29.7"),
    (46,  "Ladd McConkey",          "WR", "24.3"),
    (47,  "Chris Olave",            "WR", "25.6"),
    (48,  "Breece Hall",            "RB", "24.7"),
    (49,  "TreVeyon Henderson",     "RB", "23.3"),
    (50,  "Cam Ward",               "QB", "23.7"),
    (51,  "Jordyn Tyson",           "WR", ""),
    (52,  "Chase Brown",            "RB", "25.9"),
    (53,  "Rashee Rice",            "WR", "25.8"),
    (54,  "Quinshon Judkins",       "RB", "22.3"),
    (55,  "Saquon Barkley",         "RB", "29.0"),
    (56,  "Rome Odunze",            "WR", "23.7"),
    (57,  "Marvin Harrison Jr.",    "WR", "23.5"),
    (58,  "Brian Thomas",           "WR", "23.4"),
    (59,  "Baker Mayfield",         "QB", "30.9"),
    (60,  "Kenneth Walker",         "RB", "25.3"),
    (61,  "Kyren Williams",         "RB", "25.5"),
    (62,  "Luther Burden",          "WR", "22.2"),
    (63,  "C.J. Stroud",            "QB", "24.4"),
    (64,  "Harold Fannin",          "TE", "21.6"),
    (65,  "A.J. Brown",             "WR", "28.6"),
    (66,  "Tee Higgins",            "WR", "27.1"),
    (67,  "Sam LaPorta",            "TE", "25.1"),
    (68,  "Zay Flowers",            "WR", "25.4"),
    (69,  "Tucker Kraft",           "TE", "25.3"),
    (70,  "Jared Goff",             "QB", "31.4"),
    (71,  "Sam Darnold",            "QB", "28.7"),
    (72,  "DeVonta Smith",          "WR", "27.3"),
    (73,  "Jameson Williams",       "WR", "24.9"),
    (74,  "Tyler Shough",           "QB", "26.4"),
    (75,  "Kenyon Sadiq",           "TE", ""),
    (76,  "Josh Jacobs",            "RB", "28.0"),
    (77,  "Denzel Boston",          "WR", ""),
    (78,  "Javonte Williams",       "RB", "25.8"),
    (79,  "Jonah Coleman",          "RB", ""),
    (80,  "Kyle Pitts",             "TE", "25.4"),
    (81,  "Cam Skattebo",           "RB", "24.0"),
    (82,  "Travis Etienne",         "RB", "27.1"),
    (83,  "KC Concepcion",          "WR", ""),
    (84,  "Bryce Young",            "QB", "24.6"),
    (85,  "Kyler Murray",           "QB", "28.5"),
    (86,  "Jaylen Waddle",          "WR", "27.2"),
    (87,  "Derrick Henry",          "RB", "32.1"),
    (88,  "DJ Moore",               "WR", "28.9"),
    (89,  "Daniel Jones",           "QB", "28.7"),
    (90,  "Matthew Stafford",       "QB", "38.0"),
    (91,  "RJ Harvey",              "RB", "25.0"),
    (92,  "Jadarian Price",         "RB", ""),
    (93,  "Oronde Gadsden",         "TE", "22.7"),
    (94,  "Jordan Addison",         "WR", "24.1"),
    (95,  "Travis Hunter",          "WR", "22.8"),
    (96,  "Malik Willis",           "QB", "26.7"),
    (97,  "Ricky Pearsall",         "WR", "25.4"),
    (98,  "Davante Adams",          "WR", "33.2"),
    (99,  "Alec Pierce",            "WR", "25.8"),
    (100, "Emmett Johnson",         "RB", ""),
    (101, "Michael Wilson",         "WR", "26.0"),
    (102, "Michael Penix",          "QB", "25.8"),
    (103, "Terry McLaurin",         "WR", "30.4"),
    (104, "D'Andre Swift",          "RB", "27.1"),
    (105, "Dalton Kincaid",         "TE", "26.3"),
    (106, "Eli Stowers",            "TE", ""),
    (107, "George Kittle",          "TE", "32.4"),
    (108, "DK Metcalf",             "WR", "28.2"),
    (109, "Wan'Dale Robinson",      "WR", "25.1"),
    (110, "David Montgomery",       "RB", "28.7"),
    (111, "Matthew Golden",         "WR", "22.6"),
    (112, "J.J. McCarthy",          "QB", "23.1"),
    (113, "Ty Simpson",             "QB", ""),
    (114, "Parker Washington",      "WR", "23.9"),
    (115, "Jayden Higgins",         "WR", "23.2"),
    (116, "Omar Cooper",            "WR", ""),
    (117, "Michael Pittman",        "WR", "28.4"),
    (118, "Jake Ferguson",          "TE", "27.1"),
    (119, "Christian Watson",       "WR", "26.8"),
    (120, "Xavier Worthy",          "WR", "22.8"),
    (121, "Bhayshul Tuten",         "RB", "24.0"),
    (122, "Nicholas Singleton",     "RB", ""),
    (123, "Tyler Allgeier",         "RB", "25.8"),
    (124, "Courtland Sutton",       "WR", "30.4"),
    (125, "Jaylen Warren",          "RB", "27.3"),
    (126, "Quentin Johnston",       "WR", "24.5"),
    (127, "Shedeur Sanders",        "QB", "24.0"),
    (128, "Zach Charbonnet",        "RB", "25.1"),
    (129, "Kyle Monangai",          "RB", "23.7"),
    (130, "Elijah Sarratt",         "WR", ""),
    (131, "Mike Evans",             "WR", "32.5"),
    (132, "Brenton Strange",        "TE", "25.1"),
    (133, "Trey Benson",            "RB", "23.6"),
    (134, "Chuba Hubbard",          "RB", "26.7"),
    (135, "Jakobi Meyers",          "WR", "29.3"),
    (136, "Anthony Richardson",     "QB", "23.7"),
    (137, "Isaiah Likely",          "TE", "25.8"),
    (138, "Zachariah Branch",       "WR", ""),
    (139, "Rico Dowdle",            "RB", "27.7"),
    (140, "Mac Jones",              "QB", "27.5"),
    (141, "Theo Johnson",           "TE", "25.0"),
    (142, "Chris Bell",             "WR", ""),
    (143, "Khalil Shakir",          "WR", "26.0"),
    (144, "Brandon Aiyuk",          "WR", "27.9"),
    (145, "Rhamondre Stevenson",    "RB", "28.0"),
    (146, "Tua Tagovailoa",         "QB", "28.0"),
    (147, "Chris Brazzell",         "WR", ""),
    (148, "Josh Downs",             "WR", "24.5"),
    (149, "Blake Corum",            "RB", "25.2"),
    (150, "Romeo Doubs",            "WR", "25.9"),
    (151, "Germie Bernard",         "WR", ""),
    (152, "Kenneth Gainwell",       "RB", "26.9"),
    (153, "Troy Franklin",          "WR", "23.0"),
    (154, "Jayden Reed",            "WR", "25.8"),
    (155, "Chris Godwin",           "WR", "30.0"),
    (156, "Mike Washington",        "RB", ""),
    (157, "T.J. Hockenson",         "TE", "28.6"),
    (158, "David Njoku",            "TE", "29.6"),
    (159, "Jacory Croskey-Merritt", "RB", "24.9"),
    (160, "Rachaad White",          "RB", "27.1"),
    (161, "Demond Claiborne",       "RB", ""),
    (162, "Terrance Ferguson",      "TE", "23.0"),
    (163, "Mason Taylor",           "TE", "21.8"),
    (164, "Jalen Coker",            "WR", "24.3"),
    (165, "Jauan Jennings",         "WR", "28.6"),
    (166, "Malachi Fields",         "WR", ""),
    (167, "Pat Bryant",             "WR", "23.2"),
    (168, "AJ Barner",              "TE", "23.8"),
    (169, "Tre' Harris",            "WR", "24.0"),
    (170, "Tyreek Hill",            "WR", "32.0"),
    (171, "Jonathon Brooks",        "RB", "22.6"),
    (172, "Ja'Kobi Lane",           "WR", ""),
    (173, "J.K. Dobbins",           "RB", "27.2"),
    (174, "Kayshon Boutte",         "WR", "23.8"),
    (175, "Woody Marks",            "RB", "25.1"),
    (176, "Tony Pollard",           "RB", "28.8"),
    (177, "Mark Andrews",           "TE", "30.5"),
    (178, "Tyrone Tracy",           "RB", "26.2"),
    (179, "Max Klare",              "TE", ""),
    (180, "Braelon Allen",          "RB", "22.1"),
    (181, "Kaleb Johnson",          "RB", "22.5"),
    (182, "Antonio Williams",       "WR", ""),
    (183, "Keon Coleman",           "WR", "22.8"),
    (184, "Alvin Kamara",           "RB", "30.6"),
    (185, "Jordan Mason",           "RB", "26.7"),
    (186, "Stefon Diggs",           "WR", "32.2"),
    (187, "Deebo Samuel",           "WR", "30.1"),
    (188, "Carson Beck",            "QB", ""),
    (189, "Chimere Dike",           "WR", "24.2"),
    (190, "Jerry Jeudy",            "WR", "26.8"),
    (191, "Jalen McMillan",         "WR", "24.2"),
    (192, "Tyjae Spears",           "RB", "24.7"),
    (193, "Isaac TeSlaa",           "WR", "24.0"),
    (194, "Rashid Shaheed",         "WR", "27.5"),
    (195, "Tory Horton",            "WR", "23.2"),
    (196, "Dylan Sampson",          "RB", "21.4"),
    (197, "Adam Randall",           "RB", ""),
    (198, "Dallas Goedert",         "TE", "31.1"),
    (199, "Elic Ayomanor",          "WR", "22.7"),
    (200, "Adonai Mitchell",        "WR", "23.4"),
    (201, "Juwan Johnson",          "TE", "29.4"),
    (202, "Devin Neal",             "RB", "22.5"),
    (203, "Eric McAlister",         "WR", ""),
    (204, "Ted Hurst",              "WR", ""),
    (205, "Gunnar Helm",            "TE", "23.5"),
    (206, "Travis Kelce",           "TE", "36.4"),
    (207, "Brenen Thompson",        "WR", ""),
    (208, "Sean Tucker",            "RB", "24.3"),
    (209, "Le'Veon Moss",           "RB", ""),
    (210, "Jack Endries",           "TE", ""),
    (211, "Tank Dell",              "WR", "26.3"),
    (212, "Jaylin Noel",            "WR", "23.5"),
    (213, "Kyle Williams",          "WR", "23.3"),
    (214, "Deion Burks",            "WR", ""),
    (215, "CJ Daniels",             "WR", ""),
    (216, "Jack Bech",              "WR", "23.2"),
    (217, "J'Mari Taylor",          "RB", ""),
    (218, "Kimani Vidal",           "RB", "24.5"),
    (219, "Tank Bigsby",            "RB", "23.5"),
    (220, "Jacoby Brissett",        "QB", "33.2"),
    (221, "Taylen Green",           "QB", ""),
    (222, "CJ Donaldson",           "RB", ""),
    (223, "Dalton Schultz",         "TE", "29.6"),
    (224, "Ollie Gordon",           "RB", "22.1"),
    (225, "Isaiah Bond",            "WR", "21.9"),
    (226, "Jake Tonges",            "TE", "26.6"),
    (227, "Joe Mixon",              "RB", "29.6"),
    (228, "Oscar Delp",             "TE", ""),
    (229, "Hunter Henry",           "TE", "31.2"),
    (230, "Cade Otton",             "TE", "26.9"),
    (231, "Drew Allar",             "QB", ""),
    (232, "Aaron Jones",            "RB", "31.2"),
    (233, "James Conner",           "RB", "30.8"),
    (234, "Geno Smith",             "QB", "35.4"),
    (235, "Brian Robinson",         "RB", "26.9"),
    (236, "Noah Thomas",            "WR", ""),
    (237, "Marlin Klein",           "TE", ""),
    (238, "Dane Key",               "WR", ""),
    (239, "Pat Freiermuth",         "TE", "27.3"),
    (240, "Josh Cameron",           "WR", ""),
    (241, "Aaron Rodgers",          "QB", "42.2"),
    (242, "Tre Tucker",             "WR", "25.0"),
    (243, "Jalen Milroe",           "QB", "23.2"),
    (244, "Jaydon Blue",            "RB", "22.1"),
    (245, "Najee Harris",           "RB", "28.0"),
    (246, "Kirk Cousins",           "QB", "37.5"),
    (247, "Elijah Arroyo",          "TE", "22.9"),
    (248, "Colby Parkinson",        "TE", "27.1"),
    (249, "Isiah Pacheco",          "RB", "27.0"),
    (250, "Cade Klubnik",           "QB", ""),
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
age_updates = 0
for rank, name, pos, age in PLAYER_DATA:
    key = normalize(name)
    if key in lookup:
        row = lookup[key]
        row[SOURCE_COL] = rank
        # Backfill age only if blank and we have a value
        if age and not row.get("Age", "").strip():
            row["Age"] = age
            age_updates += 1
    else:
        new_row = {fn: "" for fn in fieldnames}
        new_row["Player"] = name
        new_row["Position"] = pos
        new_row["Age"] = age
        new_row[SOURCE_COL] = rank
        new_players.append(new_row)
        rows.append(new_row)
        lookup[key] = new_row

with open(MASTER_PATH, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Merged {len(PLAYER_DATA)} FantasyCalc players.")
print(f"  Matched: {len(PLAYER_DATA) - len(new_players)}, Age backfilled: {age_updates}")
print(f"  New players added: {len(new_players)}")
if new_players:
    for p in new_players:
        print(f"    + {p['Player']} ({p['Position']})")

subprocess.run(["python3", os.path.join(os.path.dirname(__file__), "recalculate.py"), MASTER_PATH])
