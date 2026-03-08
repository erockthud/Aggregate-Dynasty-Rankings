#!/usr/bin/env python3
"""Merge RoundBallRhettoric (Pts, Mar 2026) basketball rankings into master CSV."""

import csv
import re
import unicodedata
import subprocess

MASTER_PATH = "basketball/basketball_rankings_master.csv"
NEW_COL = "RoundBallRhettoric (Pts, Mar 2026)"

# All 228 RoundBallRhettoric rankings
RBR_RANKINGS = [
    (1,   "Victor Wembanyama",         "C",  "SAS", 22),
    (2,   "Shai Gilgeous-Alexander",   "G",  "OKC", 27),
    (3,   "Luka Dončić",               "F",  "LAL", 27),
    (4,   "Nikola Jokić",              "C",  "DEN", 31),
    (5,   "Cade Cunningham",           "G",  "DET", 24),
    (6,   "Tyrese Maxey",              "G",  "PHI", 25),
    (7,   "Anthony Edwards",           "G",  "MIN", 24),
    (8,   "Jalen Johnson",             "F",  "ATL", 24),
    (9,   "Cooper Flagg",              "F",  "DAL", 19),
    (10,  "Amen Thompson",             "G",  "HOU", 23),
    (11,  "Alperen Sengun",            "C",  "HOU", 23),
    (12,  "Jalen Williams",            "G",  "OKC", 24),
    (13,  "Scottie Barnes",            "F",  "TOR", 24),
    (14,  "Chet Holmgren",             "C",  "OKC", 23),
    (15,  "Tyrese Haliburton",         "G",  "IND", 25),
    (16,  "Jayson Tatum",              "F",  "BOS", 28),
    (17,  "Evan Mobley",               "C",  "CLE", 24),
    (18,  "Donovan Mitchell",          "G",  "CLE", 29),
    (19,  "Giannis Antetokounmpo",     "F",  "MIL", 31),
    (20,  "Trae Young",                "G",  "WAS", 27),
    (21,  "LaMelo Ball",               "G",  "CHA", 24),
    (22,  "Austin Reaves",             "G",  "LAL", 27),
    (23,  "Deni Avdija",               "F",  "POR", 25),
    (24,  "Trey Murphy III",           "G",  "NOP", 25),
    (25,  "Franz Wagner",              "F",  "ORL", 24),
    (26,  "Jaren Jackson Jr.",         "C",  "UTA", 26),
    (27,  "Devin Booker",              "G",  "PHX", 29),
    (28,  "Jamal Murray",              "G",  "DEN", 29),
    (29,  "Alex Sarr",                 "C",  "WAS", 20),
    (30,  "Karl-Anthony Towns",        "C",  "NYK", 30),
    (31,  "Jalen Brunson",             "G",  "NYK", 29),
    (32,  "Dylan Harper",              "G",  "SAS", 20),
    (33,  "Paolo Banchero",            "F",  "ORL", 23),
    (34,  "Darius Garland",            "G",  "LAC", 26),
    (35,  "Lauri Markkanen",           "C",  "UTA", 28),
    (36,  "Jalen Duren",               "C",  "DET", 22),
    (37,  "Bam Adebayo",               "C",  "MIA", 28),
    (38,  "Kon Knueppel",              "G",  "CHA", 20),
    (39,  "Josh Giddey",               "G",  "CHI", 23),
    (40,  "Brandon Miller",            "F",  "CHA", 23),
    (41,  "De'Aaron Fox",              "G",  "SAS", 28),
    (42,  "Desmond Bane",              "G",  "ORL", 27),
    (43,  "Jaylen Brown",              "G",  "BOS", 29),
    (44,  "Walker Kessler",            "C",  "UTA", 24),
    (45,  "Onyeka Okongwu",            "C",  "ATL", 25),
    (46,  "Tyler Herro",               "G",  "MIA", 26),
    (47,  "VJ Edgecombe",              "G",  "PHI", 20),
    (48,  "Domantas Sabonis",          "C",  "SAC", 29),
    (49,  "Reed Sheppard",             "G",  "HOU", 21),
    (50,  "Kel'el Ware",               "C",  "MIA", 21),
    (51,  "Stephon Castle",            "G",  "SAS", 21),
    (52,  "Derrick White",             "G",  "BOS", 31),
    (53,  "Anthony Davis",             "C",  "WAS", 32),
    (54,  "Stephen Curry",             "G",  "GSW", 37),
    (55,  "Kevin Durant",              "F",  "HOU", 37),
    (56,  "James Harden",              "G",  "CLE", 36),
    (57,  "Zion Williamson",           "F",  "NOP", 25),
    (58,  "Ja Morant",                 "G",  "MEM", 26),
    (59,  "Pascal Siakam",             "F",  "IND", 31),
    (60,  "Kyrie Irving",              "G",  "DAL", 33),
    (61,  "Jalen Suggs",               "G",  "ORL", 24),
    (62,  "Ivica Zubac",               "C",  "IND", 28),
    (63,  "Ausar Thompson",            "G",  "DET", 23),
    (64,  "Dyson Daniels",             "G",  "ATL", 22),
    (65,  "Zach Edey",                 "C",  "MEM", 23),
    (66,  "Derik Queen",               "C",  "NOP", 21),
    (67,  "Jaden McDaniels",           "F",  "MIN", 25),
    (68,  "OG Anunoby",                "F",  "NYK", 28),
    (69,  "Mikal Bridges",             "G",  "NYK", 29),
    (70,  "Keyonte George",            "G",  "UTA", 22),
    (71,  "Brandon Ingram",            "F",  "TOR", 28),
    (72,  "Jarrett Allen",             "C",  "CLE", 27),
    (73,  "Donovan Clingan",           "C",  "POR", 22),
    (74,  "Scoot Henderson",           "G",  "POR", 22),
    (75,  "Myles Turner",              "C",  "MIL", 29),
    (76,  "Dereck Lively II",          "C",  "DAL", 22),
    (77,  "Kyshawn George",            "F",  "WAS", 22),
    (78,  "Keegan Murray",             "F",  "SAC", 25),
    (79,  "Jabari Smith Jr.",           "F",  "HOU", 22),
    (80,  "Immanuel Quickley",         "G",  "TOR", 26),
    (81,  "Tari Eason",                "F",  "HOU", 24),
    (82,  "Collin Murray-Boyles",      "F",  "TOR", 20),
    (83,  "Julius Randle",             "C",  "MIN", 31),
    (84,  "Isaiah Hartenstein",        "C",  "OKC", 27),
    (85,  "Matas Buzelis",             "F",  "CHI", 21),
    (86,  "Mark Williams",             "C",  "PHX", 24),
    (87,  "Nic Claxton",               "C",  "BKN", 26),
    (88,  "Ace Bailey",                "F",  "UTA", 19),
    (89,  "Naz Reid",                  "C",  "MIN", 26),
    (90,  "Jeremiah Fears",            "G",  "NOP", 19),
    (91,  "Ryan Rollins",              "G",  "MIL", 23),
    (92,  "Shaedon Sharpe",            "G",  "POR", 22),
    (93,  "Cedric Coward",             "G",  "MEM", 22),
    (94,  "Anthony Black",             "G",  "ORL", 22),
    (95,  "Ajay Mitchell",             "G",  "OKC", 23),
    (96,  "Dejounte Murray",           "G",  "NOP", 29),
    (97,  "Devin Vassell",             "G",  "SAS", 25),
    (98,  "Coby White",                "G",  "CHA", 26),
    (99,  "Khaman Maluach",            "C",  "PHX", 19),
    (100, "Michael Porter Jr.",        "F",  "BKN", 27),
    (101, "P.J. Washington",           "F",  "DAL", 27),
    (102, "Kristaps Porziņģis",        "C",  "GSW", 30),
    (103, "Payton Pritchard",          "G",  "BOS", 28),
    (104, "Jalen Green",               "G",  "PHX", 24),
    (105, "Christian Braun",           "G",  "DEN", 24),
    (106, "Donte DiVincenzo",          "G",  "MIN", 29),
    (107, "Jordan Poole",              "G",  "NOP", 26),
    (108, "Zach LaVine",               "F",  "SAC", 30),
    (109, "LeBron James",              "F",  "LAL", 41),
    (110, "Paul George",               "F",  "PHI", 35),
    (111, "Kawhi Leonard",             "F",  "LAC", 34),
    (112, "Joel Embiid",               "C",  "PHI", 31),
    (113, "Fred VanVleet",             "G",  "HOU", 31),
    (114, "Malik Monk",                "G",  "SAC", 28),
    (115, "Peyton Watson",             "G",  "DEN", 23),
    (116, "RJ Barrett",                "F",  "TOR", 25),
    (117, "Cason Wallace",             "G",  "OKC", 22),
    (118, "Toumani Camara",            "F",  "POR", 25),
    (119, "Brandin Podziemski",        "G",  "GSW", 23),
    (120, "Nickeil Alexander-Walker",  "G",  "ATL", 27),
    (121, "Miles Bridges",             "F",  "CHA", 27),
    (122, "Cameron Johnson",           "F",  "DEN", 30),
    (123, "Andrew Nembhard",           "G",  "IND", 26),
    (124, "Herbert Jones",             "F",  "NOP", 27),
    (125, "Egor Dëmin",                "G",  "BKN", 20),
    (126, "Aaron Gordon",              "F",  "DEN", 30),
    (127, "Josh Hart",                 "G",  "NYK", 31),
    (128, "Tre Johnson",               "G",  "WAS", 20),
    (129, "Nikola Topić",              "G",  "OKC", 20),
    (130, "Mitchell Robinson",         "C",  "NYK", 27),
    (131, "Jimmy Butler III",          "F",  "GSW", 36),
    (132, "Jakob Poeltl",              "C",  "TOR", 30),
    (133, "Damian Lillard",            "G",  "POR", 34),
    (134, "Bilal Coulibaly",           "G",  "WAS", 21),
    (135, "Jaylon Tyson",              "G",  "CLE", 23),
    (136, "Jared McCain",              "G",  "OKC", 22),
    (137, "Santi Aldama",              "C",  "MEM", 25),
    (138, "John Collins",              "C",  "LAC", 28),
    (139, "Daniel Gafford",            "C",  "DAL", 27),
    (140, "Kyle Filipowski",           "C",  "UTA", 22),
    (141, "Bennedict Mathurin",        "G",  "LAC", 23),
    (142, "Jaden Ivey",                "G",  "CHI", 24),
    (143, "Ronald Holland II",         "F",  "DET", 20),
    (144, "Jonathan Kuminga",          "F",  "ATL", 23),
    (145, "Aaron Nesmith",             "G",  "IND", 26),
    (146, "Rudy Gobert",               "C",  "MIN", 33),
    (147, "Norman Powell",             "G",  "MIA", 32),
    (148, "Ryan Kalkbrenner",          "C",  "CHA", 24),
    (149, "Noah Clowney",              "C",  "BKN", 21),
    (150, "Carter Bryant",             "F",  "SAS", 20),
    (151, "Deandre Ayton",             "C",  "LAL", 27),
    (152, "Davion Mitchell",           "G",  "MIA", 27),
    (153, "Andrew Wiggins",            "F",  "MIA", 31),
    (154, "Cam Thomas",                "G",  "MIL", 24),
    (155, "Jaime Jaquez Jr.",          "G",  "MIA", 25),
    (156, "Yang Hansen",               "C",  "POR", 20),
    (157, "Thomas Sorber",             "C",  "OKC", None),
    (158, "Quentin Grimes",            "G",  "PHI", 25),
    (159, "Julian Champagnie",         "F",  "SAS", 24),
    (160, "Walter Clayton Jr.",        "G",  "MEM", 23),
    (161, "Anfernee Simons",           "G",  "CHI", 26),
    (162, "Nikola Jović",              "F",  "MIA", 22),
    (163, "Aaron Wiggins",             "G",  "OKC", 27),
    (164, "Wendell Carter Jr.",        "C",  "ORL", 26),
    (165, "Nikola Vučević",            "C",  "BOS", 35),
    (166, "DeMar DeRozan",             "G",  "SAC", 36),
    (167, "Jrue Holiday",              "G",  "POR", 35),
    (168, "Jerami Grant",              "F",  "POR", 31),
    (169, "Tobias Harris",             "F",  "DET", 33),
    (170, "Ty Jerome",                 "G",  "MEM", 28),
    (171, "Taylor Hendricks",          "F",  "MEM", 22),
    (172, "Maxime Raynaud",            "C",  "SAC", 22),
    (173, "Zaccharie Risacher",        "F",  "ATL", 20),
    (174, "Jeremy Sochan",             "F",  "NYK", 22),
    (175, "Kasparas Jakučionis",       "G",  "MIA", 19),
    (176, "CJ McCollum",               "G",  "ATL", 34),
    (177, "Draymond Green",            "F",  "GSW", 36),
    (178, "Goga Bitadze",              "C",  "ORL", 26),
    (179, "Neemias Queta",             "C",  "BOS", 26),
    (180, "Day'Ron Sharpe",            "C",  "BKN", 24),
    (181, "De'Andre Hunter",           "F",  "SAC", 28),
    (182, "Kelly Oubre Jr.",           "F",  "PHI", 30),
    (183, "Isaiah Stewart",            "C",  "DET", 24),
    (184, "Keon Ellis",                "G",  "CLE", 26),
    (185, "Jaylen Wells",              "F",  "MEM", 22),
    (186, "Jarace Walker",             "F",  "IND", 22),
    (187, "Moses Moody",               "G",  "GSW", 23),
    (188, "Rob Dillingham",            "G",  "CHI", 21),
    (189, "Bub Carrington",            "G",  "WAS", 20),
    (190, "Joan Beringer",             "F",  "MIN", 19),
    (191, "Ryan Dunn",                 "F",  "PHX", 23),
    (192, "Collin Sexton",             "G",  "CHI", 27),
    (193, "Grayson Allen",             "G",  "PHX", 30),
    (194, "Collin Gillespie",          "G",  "PHX", 26),
    (195, "Hugo González",             "G",  "BOS", 20),
    (196, "Rasheer Fleming",           "F",  "PHX", 21),
    (197, "DaRon Holmes II",           "F",  "DEN", 23),
    (198, "Ayo Dosunmu",               "G",  "MIN", 26),
    (199, "Nique Clifford",            "G",  "SAC", 24),
    (200, "Kevin Porter Jr.",          "G",  "MIL", 25),
    (201, "Isaiah Collier",            "G",  "UTA", 21),
    (202, "Jordan Walsh",              "G",  "BOS", 22),
    (203, "Bobby Portis",              "F",  "MIL", 31),
    (204, "Dillon Brooks",             "G",  "PHX", 30),
    (205, "Yves Missi",                "C",  "NOP", 21),
    (206, "Max Christie",              "G",  "DAL", 23),
    (207, "Saddiq Bey",                "G",  "NOP", 26),
    (208, "Terrence Shannon Jr.",      "F",  "MIN", 25),
    (209, "Nolan Traore",              "G",  "BKN", 19),
    (210, "Mouhamed Gueye",            "F",  "ATL", 23),
    (211, "Noa Essengue",              "F",  "CHI", 19),
    (212, "Jalen Smith",               "C",  "CHI", 25),
    (213, "Rui Hachimura",             "F",  "LAL", 28),
    (214, "Danny Wolf",                "F",  "BKN", 21),
    (215, "Isaiah Joe",                "G",  "OKC", 26),
    (216, "Cam Whitmore",              "F",  "WAS", 21),
    (217, "Alex Caruso",               "G",  "OKC", 32),
    (218, "Dennis Schröder",           "G",  "CLE", 32),
    (219, "De'Anthony Melton",         "G",  "GSW", 27),
    (220, "Devin Carter",              "G",  "SAC", 23),
    (221, "Vince Williams Jr.",        "F",  "UTA", 25),
    (222, "Tristan da Silva",          "F",  "ORL", 24),
    (223, "Robert Williams III",       "C",  "POR", 28),
    (224, "Jake LaRavia",              "F",  "LAL", 24),
    (225, "Noah Penda",                "G",  "ORL", 21),
    (226, "Ryan Nembhard",             "G",  "DAL", 22),
    (227, "Luguentz Dort",             "G",  "OKC", 26),
    (228, "Gradey Dick",               "G",  "TOR", 22),
]


def normalize(name):
    name = unicodedata.normalize("NFKD", name)
    name = name.encode("ascii", "ignore").decode("ascii")
    name = name.lower()
    name = re.sub(r"\b(jr|sr|ii|iii|iv|v)\b\.?", "", name)
    name = re.sub(r"[^a-z\s]", "", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name


def main():
    rbr_lookup = {}
    for rank, name, pos, team, age in RBR_RANKINGS:
        key = normalize(name)
        rbr_lookup[key] = (rank, name, pos, team, age)

    with open(MASTER_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)
        rows = list(reader)

    avg_rank_idx = fieldnames.index("Average Rank")
    new_fieldnames = fieldnames[:avg_rank_idx] + [NEW_COL] + fieldnames[avg_rank_idx:]

    matched_keys = set()

    for row in rows:
        key = normalize(row["Player"])
        if key in rbr_lookup:
            rank, _, _, _, _ = rbr_lookup[key]
            row[NEW_COL] = rank
            matched_keys.add(key)
        else:
            row[NEW_COL] = ""

    unmatched = []
    for rank, name, pos, team, age in RBR_RANKINGS:
        key = normalize(name)
        if key not in matched_keys:
            unmatched.append((rank, name, pos, team, age))

    print(f"Matched: {len(matched_keys)} players")
    print(f"New players to add: {len(unmatched)}")
    for rank, name, pos, team, age in unmatched:
        print(f"  [{rank}] {name} ({pos}, {team})")

    nba_teams = {
        "ATL","BKN","BOS","CHA","CHI","CLE","DAL","DEN","DET","GSW",
        "HOU","IND","LAC","LAL","MEM","MIA","MIL","MIN","NOP","NYK",
        "OKC","ORL","PHI","PHX","POR","SAC","SAS","TOR","UTA","WAS",
    }

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

    with open(MASTER_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=new_fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nWrote {len(rows)} rows to {MASTER_PATH}")

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
