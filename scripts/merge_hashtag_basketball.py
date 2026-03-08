#!/usr/bin/env python3
"""Merge Hashtag Basketball (Joseph Mamone, Pts, Feb 2026) rankings into master CSV."""

import csv
import re
import unicodedata
import subprocess

MASTER_PATH = "basketball/basketball_rankings_master.csv"
NEW_COL = "Hashtag Basketball (Pts, Feb 2026)"

# All 250 Hashtag Basketball rankings with canonical names
HASHTAG_RANKINGS = [
    (1,   "Victor Wembanyama",         "C",    "SAS", 22),
    (2,   "Shai Gilgeous-Alexander",   "G",    "OKC", 27),
    (3,   "Luka Dončić",               "G",    "LAL", 27),
    (4,   "Nikola Jokić",              "C",    "DEN", 31),
    (5,   "Giannis Antetokounmpo",     "F",    "MIL", 31),
    (6,   "Cade Cunningham",           "G",    "DET", 24),
    (7,   "Cooper Flagg",              "F",    "DAL", 19),
    (8,   "Tyrese Maxey",              "G",    "PHI", 25),
    (9,   "Anthony Edwards",           "G",    "MIN", 24),
    (10,  "Scottie Barnes",            "F",    "TOR", 24),
    (11,  "Alperen Sengun",            "C",    "HOU", 23),
    (12,  "Jalen Johnson",             "F",    "ATL", 24),
    (13,  "Evan Mobley",               "C",    "CLE", 24),
    (14,  "Chet Holmgren",             "C",    "OKC", 23),
    (15,  "Jalen Williams",            "G",    "OKC", 24),
    (16,  "Donovan Mitchell",          "G",    "CLE", 29),
    (17,  "Trae Young",                "G",    "WAS", 27),
    (18,  "Jayson Tatum",              "F",    "BOS", 28),
    (19,  "Tyrese Haliburton",         "G",    "IND", 26),
    (20,  "Amen Thompson",             "G",    "HOU", 23),
    (21,  "Devin Booker",              "G",    "PHX", 29),
    (22,  "Franz Wagner",              "F",    "ORL", 24),
    (23,  "Paolo Banchero",            "F",    "ORL", 23),
    (24,  "Josh Giddey",               "G",    "CHI", 23),
    (25,  "Alex Sarr",                 "C",    "WAS", 20),
    (26,  "Deni Avdija",               "F",    "POR", 25),
    (27,  "Trey Murphy III",           "G",    "NOP", 25),
    (28,  "Austin Reaves",             "G",    "LAL", 27),
    (29,  "Karl-Anthony Towns",        "C",    "NYK", 30),
    (30,  "Jamal Murray",              "G",    "DEN", 29),
    (31,  "Jaren Jackson Jr.",         "C",    "UTA", 26),
    (32,  "Kon Knueppel",              "G",    "CHA", 20),
    (33,  "Jalen Brunson",             "G",    "NYK", 29),
    (34,  "LaMelo Ball",               "G",    "CHA", 24),
    (35,  "De'Aaron Fox",              "G",    "SAS", 28),
    (36,  "Jalen Duren",               "C",    "DET", 22),
    (37,  "Zion Williamson",           "F",    "NOP", 25),
    (38,  "Stephon Castle",            "G",    "SAS", 21),
    (39,  "Domantas Sabonis",          "C",    "SAC", 29),
    (40,  "Jaylen Brown",              "G",    "BOS", 29),
    (41,  "Keyonte George",            "G",    "UTA", 22),
    (42,  "Dylan Harper",              "G",    "SAS", 20),
    (43,  "Michael Porter Jr.",        "F",    "BKN", 27),
    (44,  "Darius Garland",            "G",    "LAC", 26),
    (45,  "James Harden",              "G",    "CLE", 36),
    (46,  "Stephen Curry",             "G",    "GSW", 38),
    (47,  "Bam Adebayo",               "C",    "MIA", 28),
    (48,  "Tyler Herro",               "G",    "MIA", 26),
    (49,  "RJ Barrett",                "F",    "TOR", 25),
    (50,  "VJ Edgecombe",              "G",    "PHI", 20),
    (51,  "Ivica Zubac",               "C",    "IND", 29),
    (52,  "Onyeka Okongwu",            "C",    "ATL", 25),
    (53,  "Pascal Siakam",             "F",    "IND", 31),
    (54,  "Lauri Markkanen",           "C",    "UTA", 28),
    (55,  "Matas Buzelis",             "F",    "CHI", 21),
    (56,  "Mikal Bridges",             "G",    "NYK", 29),
    (57,  "Anthony Davis",             "C",    "WAS", 33),
    (58,  "Zach Edey",                 "C",    "MEM", 23),
    (59,  "Brandon Miller",            "F",    "CHA", 23),
    (60,  "Desmond Bane",              "G",    "ORL", 27),
    (61,  "OG Anunoby",                "F",    "NYK", 28),
    (62,  "Brandon Ingram",            "F",    "TOR", 28),
    (63,  "Kevin Durant",              "F",    "HOU", 37),
    (64,  "Keegan Murray",             "F",    "SAC", 25),
    (65,  "Jalen Green",               "G",    "PHX", 24),
    (66,  "Scoot Henderson",           "G",    "POR", 22),
    (67,  "Donovan Clingan",           "C",    "POR", 22),
    (68,  "Ja Morant",                 "G",    "MEM", 26),
    (69,  "Fred VanVleet",             "G",    "HOU", 32),
    (70,  "Julius Randle",             "C",    "MIN", 31),
    (71,  "Derrick White",             "G",    "BOS", 31),
    (72,  "Derik Queen",               "C",    "NOP", 21),
    (73,  "Kyshawn George",            "F",    "WAS", 22),
    (74,  "Nic Claxton",               "C",    "BKN", 26),
    (75,  "Reed Sheppard",             "G",    "HOU", 21),
    (76,  "Isaiah Hartenstein",        "C",    "OKC", 27),
    (77,  "Immanuel Quickley",         "G",    "TOR", 26),
    (78,  "Dyson Daniels",             "G",    "ATL", 23),
    (79,  "Walker Kessler",            "C",    "UTA", 24),
    (80,  "Deandre Ayton",             "C",    "LAL", 27),
    (81,  "Jalen Suggs",               "G",    "ORL", 24),
    (82,  "Anthony Black",             "G",    "ORL", 22),
    (83,  "Jabari Smith Jr.",           "F",    "HOU", 22),
    (84,  "Mark Williams",             "C",    "PHX", 24),
    (85,  "Norman Powell",             "G",    "MIA", 32),
    (86,  "Collin Murray-Boyles",      "F",    "TOR", 20),
    (87,  "Ryan Kalkbrenner",          "C",    "CHA", 24),
    (88,  "Kyrie Irving",              "G",    "DAL", 34),
    (89,  "Kel'el Ware",               "C",    "MIA", 21),
    (90,  "Joel Embiid",               "C",    "PHI", 32),
    (91,  "Myles Turner",              "C",    "MIL", 30),
    (92,  "Zach LaVine",               "F",    "SAC", 31),
    (93,  "Coby White",                "G",    "CHA", 26),
    (94,  "Ace Bailey",                "F",    "UTA", 19),
    (95,  "Dejounte Murray",           "G",    "NOP", 29),
    (96,  "Cam Thomas",                "G",    "MIL", 24),
    (97,  "Kristaps Porziņģis",        "C",    "GSW", 30),
    (98,  "Jeremiah Fears",            "G",    "NOP", 19),
    (99,  "Tre Johnson",               "G",    "WAS", 20),
    (100, "Christian Braun",           "G",    "DEN", 24),
    (101, "Rudy Gobert",               "C",    "MIN", 33),
    (102, "Kawhi Leonard",             "F",    "LAC", 34),
    (103, "Naz Reid",                  "C",    "MIN", 26),
    (104, "Jarrett Allen",             "C",    "CLE", 27),
    (105, "Miles Bridges",             "F",    "CHA", 28),
    (106, "Jakob Poeltl",              "C",    "TOR", 30),
    (107, "Peyton Watson",             "G",    "DEN", 23),
    (108, "Bub Carrington",            "G",    "WAS", 20),
    (109, "Jaden McDaniels",           "F",    "MIN", 25),
    (110, "Bilal Coulibaly",           "G",    "WAS", 21),
    (111, "Toumani Camara",            "F",    "POR", 25),
    (112, "Nickeil Alexander-Walker",  "G",    "ATL", 27),
    (113, "Jaylen Wells",              "F",    "MEM", 22),
    (114, "Paul George",               "F",    "PHI", 35),
    (115, "Shaedon Sharpe",            "G",    "POR", 22),
    (116, "Kevin Porter Jr.",          "G",    "MIL", 25),
    (117, "Devin Vassell",             "G",    "SAS", 25),
    (118, "Ausar Thompson",            "G",    "DET", 23),
    (119, "Jordan Poole",              "G",    "NOP", 26),
    (120, "Tari Eason",                "F",    "HOU", 24),
    (121, "Payton Pritchard",          "G",    "BOS", 28),
    (122, "Cedric Coward",             "G",    "MEM", 22),
    (123, "Josh Hart",                 "G",    "NYK", 31),
    (124, "Jaylon Tyson",              "G",    "CLE", 23),
    (125, "DeMar DeRozan",             "G",    "SAC", 36),
    (126, "Moussa Diabaté",            "F",    "CHA", 24),
    (127, "LeBron James",              "F",    "LAL", 41),
    (128, "Andrew Nembhard",           "G",    "IND", 26),
    (129, "Kyle Filipowski",           "C",    "UTA", 22),
    (130, "Santi Aldama",              "C",    "MEM", 25),
    (131, "Ajay Mitchell",             "G",    "OKC", 23),
    (132, "Brandin Podziemski",        "G",    "GSW", 23),
    (133, "Isaiah Collier",            "G",    "UTA", 21),
    (134, "Cameron Johnson",           "F",    "DEN", 30),
    (135, "Egor Dëmin",                "G",    "BKN", 20),
    (136, "Zaccharie Risacher",        "F",    "ATL", 20),
    (137, "Malik Monk",                "G",    "SAC", 28),
    (138, "Isaiah Stewart",            "C",    "DET", 24),
    (139, "Dereck Lively II",          "C",    "DAL", 22),
    (140, "Jaden Ivey",                "G",    "CHI", 24),
    (141, "Nikola Vučević",            "C",    "BOS", 35),
    (142, "Aaron Nesmith",             "G",    "IND", 26),
    (143, "Jaime Jaquez Jr.",          "G",    "MIA", 25),
    (144, "Wendell Carter Jr.",        "C",    "ORL", 26),
    (145, "Collin Gillespie",          "G",    "PHX", 26),
    (146, "Yanic Konan Niederhauser",  "C",    "LAC", 23),
    (147, "Khaman Maluach",            "C",    "PHX", 19),
    (148, "Herbert Jones",             "F",    "NOP", 27),
    (149, "Davion Mitchell",           "G",    "MIA", 27),
    (150, "P.J. Washington",           "F",    "DAL", 27),
    (151, "Anfernee Simons",           "G",    "CHI", 26),
    (152, "Isaiah Jackson",            "F",    "LAC", 24),
    (153, "Brice Sensabaugh",          "F",    "UTA", 22),
    (154, "Bennedict Mathurin",        "G",    "LAC", 23),
    (155, "Aaron Gordon",              "F",    "DEN", 30),
    (156, "Grayson Allen",             "G",    "PHX", 30),
    (157, "Jarace Walker",             "F",    "IND", 22),
    (158, "Jonathan Kuminga",          "F",    "ATL", 23),
    (159, "Ayo Dosunmu",               "G",    "MIN", 26),
    (160, "Jimmy Butler III",          "F",    "GSW", 36),
    (161, "Donte DiVincenzo",          "G",    "MIN", 29),
    (162, "Rui Hachimura",             "F",    "LAL", 28),
    (163, "Damian Lillard",            "G",    "POR", 35),
    (164, "Max Christie",              "G",    "DAL", 23),
    (165, "Dillon Brooks",             "G",    "PHX", 30),
    (166, "Caris LeVert",              "G",    "DET", 31),
    (167, "Noah Clowney",              "C",    "BKN", 21),
    (168, "Jared McCain",              "G",    "OKC", 22),
    (169, "John Collins",              "C",    "LAC", 28),
    (170, "Maxime Raynaud",            "C",    "SAC", 22),
    (171, "Will Riley",                "F",    "WAS", 20),
    (172, "Nique Clifford",            "G",    "SAC", 24),
    (173, "Jalen Smith",               "C",    "CHI", 26),
    (174, "Ryan Rollins",              "G",    "MIL", 23),
    (175, "Cason Wallace",             "G",    "OKC", 22),
    (176, "Mitchell Robinson",         "C",    "NYK", 27),
    (177, "Jay Huff",                  "C",    "IND", 28),
    (178, "Collin Sexton",             "G",    "CHI", 27),
    (179, "Jake LaRavia",              "F",    "LAL", 24),
    (180, "Nikola Jović",              "F",    "MIA", 22),
    (181, "Ronald Holland II",         "F",    "DET", 20),
    (182, "Cam Whitmore",              "F",    "WAS", 21),
    (183, "Max Strus",                 "G",    "CLE", 29),
    (184, "Cam Spencer",               "G",    "MEM", 25),
    (185, "GG Jackson",                "F",    "MEM", 21),
    (186, "Kasparas Jakučionis",       "G",    "MIA", 19),
    (187, "Jerami Grant",              "F",    "POR", 32),
    (188, "Obi Toppin",                "F",    "IND", 28),
    (189, "Drake Powell",              "G",    "BKN", 20),
    (190, "Daniel Gafford",            "C",    "DAL", 27),
    (191, "Thomas Sorber",             "C",    "OKC", None),
    (192, "Saddiq Bey",                "G",    "NOP", 26),
    (193, "Carter Bryant",             "F",    "SAS", 20),
    (194, "De'Anthony Melton",         "G",    "GSW", 27),
    (195, "Neemias Queta",             "C",    "BOS", 26),
    (196, "Jrue Holiday",              "G",    "POR", 35),
    (197, "Taylor Hendricks",          "F",    "MEM", 22),
    (198, "Naji Marshall",             "F",    "DAL", 28),
    (199, "Tobias Harris",             "F",    "DET", 33),
    (200, "Yang Hansen",               "C",    "POR", 20),
    (201, "Jusuf Nurkić",              "C",    "UTA", 31),
    (202, "Cody Williams",             "F",    "UTA", 21),
    (203, "Sandro Mamukelashvili",     "C",    "TOR", 26),
    (204, "Kelly Oubre Jr.",           "F",    "PHI", 30),
    (205, "Dylan Cardwell",            "C",    "SAC", 24),
    (206, "Ousmane Dieng",             "F",    "MIL", 22),
    (207, "Quentin Grimes",            "G",    "PHI", 25),
    (208, "Ryan Dunn",                 "F",    "PHX", 23),
    (209, "CJ McCollum",               "G",    "ATL", 34),
    (210, "Jamal Shead",               "G",    "TOR", 23),
    (211, "Sion James",                "G",    "CHA", 23),
    (212, "Miles McBride",             "G",    "NYK", 25),
    (213, "Josh Minott",               "F",    "BKN", 23),
    (214, "Justin Champagnie",         "G",    "WAS", 24),
    (215, "Luke Kornet",               "C",    "SAS", 30),
    (216, "Keon Ellis",                "G",    "CLE", 26),
    (217, "Yves Missi",                "C",    "NOP", 21),
    (218, "Pelle Larsson",             "G",    "MIA", 25),
    (219, "D'Angelo Russell",          "G",    "WAS", 30),
    (220, "Bradley Beal",              "G",    "LAC", 32),
    (221, "Andrew Wiggins",            "F",    "MIA", 31),
    (222, "Draymond Green",            "F",    "GSW", 36),
    (223, "Gradey Dick",               "G",    "TOR", 22),
    (224, "Jordan Walsh",              "G",    "BOS", 22),
    (225, "Leonard Miller",            "F",    "CHI", 22),
    (226, "Luke Kennard",              "G",    "LAL", 29),
    (227, "Moussa Cisse",              "C",    "DAL", None),
    (228, "Terrence Shannon Jr.",      "F",    "MIN", 25),
    (229, "Goga Bitadze",              "C",    "ORL", 26),
    (230, "Aaron Wiggins",             "G",    "OKC", 27),
    (231, "Noa Essengue",              "F",    "CHI", 19),
    (232, "Ryan Nembhard",             "G",    "DAL", 23),
    (233, "Walter Clayton Jr.",        "G",    "MEM", 23),
    (234, "Danny Wolf",                "F",    "BKN", 21),
    (235, "De'Andre Hunter",           "F",    "SAC", 28),
    (236, "Kyle Kuzma",                "F",    "MIL", 30),
    (237, "Gary Trent Jr.",            "G",    "MIL", 27),
    (238, "Luguentz Dort",             "G",    "OKC", 26),
    (239, "Russell Westbrook",         "G",    "SAC", 37),
    (240, "Scotty Pippen Jr.",         "G",    "MEM", 25),
    (241, "Bobby Portis",              "F",    "MIL", 31),
    (242, "Adem Bona",                 "F",    "PHI", 22),
    (243, "Moses Moody",               "G",    "GSW", 23),
    (244, "Cole Anthony",              "G",    "PHX", 25),
    (245, "Daniss Jenkins",            "G",    "DET", 24),
    (246, "Dru Smith",                 "G",    "MIA", 28),
    (247, "Keldon Johnson",            "F",    "SAS", 26),
    (248, "Pat Spencer",               "G",    "GSW", 29),
    (249, "Johnny Furphy",             "G",    "IND", 21),
    (250, "Dennis Schröder",           "G",    "CLE", 32),
]


def normalize(name):
    """Normalize name to ASCII lowercase, stripping suffixes and punctuation."""
    name = unicodedata.normalize("NFKD", name)
    name = name.encode("ascii", "ignore").decode("ascii")
    name = name.lower()
    name = re.sub(r"\b(jr|sr|ii|iii|iv|v)\b\.?", "", name)
    name = re.sub(r"[^a-z\s]", "", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name


def main():
    # Build Hashtag lookup: normalized_name -> (rank, pos, team, age)
    hashtag_lookup = {}
    for rank, name, pos, team, age in HASHTAG_RANKINGS:
        key = normalize(name)
        hashtag_lookup[key] = (rank, name, pos, team, age)

    # Read master
    with open(MASTER_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)
        rows = list(reader)

    # Insert new column before "Average Rank"
    avg_rank_idx = fieldnames.index("Average Rank")
    new_fieldnames = fieldnames[:avg_rank_idx] + [NEW_COL] + fieldnames[avg_rank_idx:]

    # Track matched keys
    matched_keys = set()

    # Update existing rows
    for row in rows:
        key = normalize(row["Player"])
        if key in hashtag_lookup:
            rank, _, _, _, _ = hashtag_lookup[key]
            row[NEW_COL] = rank
            matched_keys.add(key)
        else:
            row[NEW_COL] = ""

    # Find unmatched Hashtag players
    unmatched = []
    for rank, name, pos, team, age in HASHTAG_RANKINGS:
        key = normalize(name)
        if key not in matched_keys:
            unmatched.append((rank, name, pos, team, age))

    print(f"Matched: {len(matched_keys)} players")
    print(f"New players to add: {len(unmatched)}")
    for rank, name, pos, team, age in unmatched:
        print(f"  [{rank}] {name} ({pos}, {team})")

    # NBA teams set for Level detection
    nba_teams = {
        "ATL","BKN","BOS","CHA","CHI","CLE","DAL","DEN","DET","GSW",
        "HOU","IND","LAC","LAL","MEM","MIA","MIL","MIN","NOP","NYK",
        "OKC","ORL","PHI","PHX","POR","SAC","SAS","TOR","UTA","WAS",
    }

    # Add new rows for unmatched players
    for rank, name, pos, team, age in unmatched:
        team_val = team if team else ""
        level = "NBA" if team_val in nba_teams else "College"
        age_val = str(age) if age else ""

        new_row = {fn: "" for fn in new_fieldnames}
        new_row["Player"] = name
        new_row["Position"] = pos
        new_row["Team"] = team_val
        new_row["Age"] = age_val
        new_row["Level"] = level
        new_row[NEW_COL] = rank
        rows.append(new_row)

    # Write back
    with open(MASTER_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=new_fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nWrote {len(rows)} rows to {MASTER_PATH}")

    # Recalculate
    print("\nRunning recalculate.py...")
    result = subprocess.run(
        ["python3", "scripts/recalculate.py", MASTER_PATH],
        capture_output=True, text=True
    )
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)


if __name__ == "__main__":
    main()
