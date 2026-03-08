#!/usr/bin/env python3
"""Merge Matt Lawson (Pts, Mar 2026) basketball rankings into the master CSV."""

import csv
import re
import unicodedata
import subprocess

MASTER_PATH = "basketball/basketball_rankings_master.csv"
NEW_COL = "Matt Lawson (Pts, Mar 2026)"

# All 300 Matt Lawson rankings with canonical names
LAWSON_RANKINGS = [
    (1, "Victor Wembanyama", "C", "SAS", 22),
    (2, "Shai Gilgeous-Alexander", "G", "OKC", 27),
    (3, "Nikola Jokić", "C", "DEN", 31),
    (4, "Luka Dončić", "F", "LAL", 27),
    (5, "Cooper Flagg", "F", "DAL", 19),
    (6, "Cade Cunningham", "G", "DET", 24),
    (7, "Tyrese Maxey", "G", "PHI", 25),
    (8, "Anthony Edwards", "G", "MIN", 24),
    (9, "Jalen Johnson", "F", "ATL", 24),
    (10, "Jalen Williams", "G", "OKC", 24),
    (11, "Alperen Sengun", "C", "HOU", 23),
    (12, "Chet Holmgren", "C", "OKC", 23),
    (13, "Evan Mobley", "C", "CLE", 24),
    (14, "Amen Thompson", "G", "HOU", 23),
    (15, "Tyrese Haliburton", "G", "IND", 25),
    (16, "Jayson Tatum", "F", "BOS", 28),
    (17, "Giannis Antetokounmpo", "F", "MIL", 31),
    (18, "Cameron Boozer", "F", "Duke", None),
    (19, "Darryn Peterson", "G", "Kansas", None),
    (20, "Scottie Barnes", "F", "TOR", 24),
    (21, "Franz Wagner", "F", "ORL", 24),
    (22, "Trae Young", "G", "WAS", 27),
    (23, "Donovan Mitchell", "G", "CLE", 29),
    (24, "Austin Reaves", "G", "LAL", 27),
    (25, "Devin Booker", "G", "PHX", 29),
    (26, "Jalen Brunson", "G", "NYK", 29),
    (27, "Dylan Harper", "G", "SAS", 20),
    (28, "AJ Dybantsa", "F", "BYU", None),
    (29, "Deni Avdija", "F", "POR", 25),
    (30, "LaMelo Ball", "G", "CHA", 24),
    (31, "Josh Giddey", "G", "CHI", 23),
    (32, "Paolo Banchero", "F", "ORL", 23),
    (33, "Karl-Anthony Towns", "C", "NYK", 30),
    (34, "Alex Sarr", "C", "WAS", 20),
    (35, "Trey Murphy III", "G", "NOP", 25),
    (36, "Jalen Duren", "C", "DET", 22),
    (37, "Darius Garland", "G", "LAC", 26),
    (38, "De'Aaron Fox", "G", "SAS", 28),
    (39, "Jaren Jackson Jr.", "C", "UTA", 26),
    (40, "Jamal Murray", "G", "DEN", 29),
    (41, "Bam Adebayo", "C", "MIA", 28),
    (42, "Jaylen Brown", "G", "BOS", 29),
    (43, "Kon Knueppel", "G", "CHA", 20),
    (44, "Tyler Herro", "G", "MIA", 26),
    (45, "Domantas Sabonis", "C", "SAC", 29),
    (46, "Anthony Davis", "C", "WAS", 32),
    (47, "VJ Edgecombe", "G", "PHI", 20),
    (48, "Desmond Bane", "G", "ORL", 27),
    (49, "Lauri Markkanen", "C", "UTA", 28),
    (50, "Kevin Durant", "F", "HOU", 37),
    (51, "James Harden", "G", "CLE", 36),
    (52, "Zach Edey", "C", "MEM", 23),
    (53, "Stephen Curry", "G", "GSW", 37),
    (54, "Brandon Miller", "F", "CHA", 23),
    (55, "Ivica Zubac", "C", "IND", 28),
    (56, "Caleb Wilson", "F", "North Carolina", None),
    (57, "Kingston Flemings", "G", "Houston", None),
    (58, "Pascal Siakam", "F", "IND", 31),
    (59, "Stephon Castle", "G", "SAS", 21),
    (60, "Dyson Daniels", "G", "ATL", 22),
    (61, "Derik Queen", "C", "NOP", 21),
    (62, "Kel'el Ware", "C", "MIA", 21),
    (63, "Zion Williamson", "F", "NOP", 25),
    (64, "Ja Morant", "G", "MEM", 26),
    (65, "Ausar Thompson", "G", "DET", 23),
    (66, "Onyeka Okongwu", "C", "ATL", 25),
    (67, "Matas Buzelis", "F", "CHI", 21),
    (68, "OG Anunoby", "F", "NYK", 28),
    (69, "Mikel Brown Jr.", "G", "Louisville", None),
    (70, "Isaiah Hartenstein", "C", "OKC", 27),
    (71, "Kyrie Irving", "G", "DAL", 33),
    (72, "Derrick White", "G", "BOS", 31),
    (73, "Mikal Bridges", "G", "NYK", 29),
    (74, "Reed Sheppard", "G", "HOU", 21),
    (75, "Ace Bailey", "F", "UTA", 19),
    (76, "Walker Kessler", "C", "UTA", 24),
    (77, "Scoot Henderson", "G", "POR", 22),
    (78, "Brandon Ingram", "F", "TOR", 28),
    (79, "Jeremiah Fears", "G", "NOP", 19),
    (80, "Jayden Quaintance", "C", "Kentucky", None),
    (81, "Jarrett Allen", "C", "CLE", 27),
    (82, "Keyonte George", "G", "UTA", 22),
    (83, "Kyshawn George", "F", "WAS", 22),
    (84, "Immanuel Quickley", "G", "TOR", 26),
    (85, "Myles Turner", "C", "MIL", 29),
    (86, "Cedric Coward", "G", "MEM", 22),
    (87, "Joel Embiid", "C", "PHI", 31),
    (88, "Jaden McDaniels", "F", "MIN", 25),
    (89, "Jalen Suggs", "G", "ORL", 24),
    (90, "Coby White", "G", "CHA", 26),
    (91, "Donovan Clingan", "C", "POR", 22),
    (92, "Tari Eason", "F", "HOU", 24),
    (93, "Julius Randle", "C", "MIN", 31),
    (94, "Mark Williams", "C", "PHX", 24),
    (95, "Michael Porter Jr.", "F", "BKN", 27),
    (96, "Jared McCain", "G", "OKC", 22),
    (97, "Jakob Poeltl", "C", "TOR", 30),
    (98, "Jalen Green", "G", "PHX", 24),
    (99, "Shaedon Sharpe", "G", "POR", 22),
    (100, "Jordan Poole", "G", "NOP", 26),
    (101, "Nic Claxton", "C", "BKN", 26),
    (102, "Kawhi Leonard", "F", "LAC", 34),
    (103, "Zach LaVine", "F", "SAC", 30),
    (104, "Naz Reid", "C", "MIN", 26),
    (105, "Tre Johnson", "G", "WAS", 19),
    (106, "Kristaps Porziņģis", "C", "GSW", 30),
    (107, "Ryan Rollins", "G", "MIL", 23),
    (108, "Egor Dëmin", "G", "BKN", 20),
    (109, "Keegan Murray", "F", "SAC", 25),
    (110, "Jabari Smith Jr.", "F", "HOU", 22),
    (111, "Payton Pritchard", "G", "BOS", 28),
    (112, "P.J. Washington", "F", "DAL", 27),
    (113, "Dereck Lively II", "C", "DAL", 22),
    (114, "Miles Bridges", "F", "CHA", 27),
    (115, "Devin Vassell", "G", "SAS", 25),
    (116, "Andrew Nembhard", "G", "IND", 26),
    (117, "LeBron James", "F", "LAL", 41),
    (118, "Christian Braun", "G", "DEN", 24),
    (119, "Toumani Camara", "F", "POR", 25),
    (120, "Collin Murray-Boyles", "F", "TOR", 20),
    (121, "Josh Hart", "G", "NYK", 30),
    (122, "Ronald Holland II", "F", "DET", 20),
    (123, "Jimmy Butler III", "F", "GSW", 36),
    (124, "Ryan Kalkbrenner", "C", "CHA", 24),
    (125, "Deandre Ayton", "C", "LAL", 27),
    (126, "Santi Aldama", "C", "MEM", 25),
    (127, "Khaman Maluach", "C", "PHX", 19),
    (128, "Ajay Mitchell", "G", "OKC", 23),
    (129, "Anthony Black", "G", "ORL", 22),
    (130, "Jonathan Kuminga", "F", "ATL", 23),
    (131, "Cason Wallace", "G", "OKC", 22),
    (132, "Dejounte Murray", "G", "NOP", 29),
    (133, "RJ Barrett", "F", "TOR", 25),
    (134, "Aaron Gordon", "F", "DEN", 30),
    (135, "Brandin Podziemski", "G", "GSW", 23),
    (136, "Malik Monk", "G", "SAC", 28),
    (137, "Bilal Coulibaly", "G", "WAS", 21),
    (138, "Nikola Topić", "G", "OKC", 20),
    (139, "Daniel Gafford", "C", "DAL", 27),
    (140, "Nickeil Alexander-Walker", "G", "ATL", 27),
    (141, "Cameron Johnson", "F", "DEN", 29),
    (142, "Anfernee Simons", "G", "CHI", 26),
    (143, "Paul George", "F", "PHI", 35),
    (144, "Bennedict Mathurin", "G", "LAC", 23),
    (145, "Quentin Grimes", "G", "PHI", 25),
    (146, "Isaiah Collier", "G", "UTA", 21),
    (147, "Cam Thomas", "G", "MIL", 24),
    (148, "John Collins", "C", "LAC", 28),
    (149, "Rudy Gobert", "C", "MIN", 33),
    (150, "Jaime Jaquez Jr.", "G", "MIA", 25),
    (151, "Thomas Sorber", "C", "OKC", None),
    (152, "Kyle Filipowski", "C", "UTA", 22),
    (153, "Norman Powell", "G", "MIA", 32),
    (154, "Jaden Ivey", "G", "CHI", 24),
    (155, "Fred VanVleet", "G", "HOU", 31),
    (156, "Zaccharie Risacher", "F", "ATL", 20),
    (157, "Herbert Jones", "F", "NOP", 27),
    (158, "Donte DiVincenzo", "G", "MIN", 29),
    (159, "Ty Jerome", "G", "MEM", 28),
    (160, "Aaron Nesmith", "G", "IND", 26),
    (161, "Joan Beringer", "F", "MIN", 19),
    (162, "Nikola Jović", "F", "MIA", 22),
    (163, "Jaylon Tyson", "G", "CLE", 23),
    (164, "Nique Clifford", "G", "SAC", 24),
    (165, "Walter Clayton Jr.", "G", "MEM", 22),
    (166, "Jase Richardson", "G", "ORL", 20),
    (167, "Maxime Raynaud", "C", "SAC", 22),
    (168, "Keon Ellis", "G", "CLE", 26),
    (169, "Nikola Vučević", "C", "BOS", 35),
    (170, "Jrue Holiday", "G", "POR", 35),
    (171, "Kasparas Jakučionis", "G", "MIA", 19),
    (172, "Damian Lillard", "G", "POR", 34),
    (173, "Noa Essengue", "F", "CHI", 19),
    (174, "Max Christie", "G", "DAL", 23),
    (175, "Rob Dillingham", "G", "CHI", 21),
    (176, "Carter Bryant", "F", "SAS", 20),
    (177, "De'Andre Hunter", "F", "SAC", 28),
    (178, "Scotty Pippen Jr.", "G", "MEM", 25),
    (179, "Andrew Wiggins", "F", "MIA", 31),
    (180, "Josh Minott", "F", "BKN", 23),
    (181, "Jaylen Wells", "F", "MEM", 22),
    (182, "Neemias Queta", "C", "BOS", 26),
    (183, "Yang Hansen", "C", "POR", 20),
    (184, "Dillon Brooks", "G", "PHX", 30),
    (185, "Jeremy Sochan", "F", "NYK", 22),
    (186, "Isaiah Stewart", "C", "DET", 24),
    (187, "Davion Mitchell", "G", "MIA", 27),
    (188, "Hugo González", "G", "BOS", 20),
    (189, "Danny Wolf", "F", "BKN", 21),
    (190, "Noah Clowney", "C", "BKN", 21),
    (191, "Kevin Porter Jr.", "G", "MIL", 25),
    (192, "Jerami Grant", "F", "POR", 31),
    (193, "CJ McCollum", "G", "ATL", 34),
    (194, "Jake LaRavia", "F", "LAL", 24),
    (195, "Ryan Dunn", "F", "PHX", 23),
    (196, "Kyle Kuzma", "F", "MIL", 30),
    (197, "Moussa Diabaté", "F", "CHA", 24),
    (198, "Aaron Wiggins", "G", "OKC", 27),
    (199, "DeMar DeRozan", "G", "SAC", 36),
    (200, "Goga Bitadze", "C", "ORL", 26),
    (201, "Collin Sexton", "G", "CHI", 27),
    (202, "Luke Kornet", "C", "SAS", 30),
    (203, "Draymond Green", "F", "GSW", 35),
    (204, "Peyton Watson", "G", "DEN", 23),
    (205, "Moses Moody", "G", "GSW", 23),
    (206, "Ayo Dosunmu", "G", "MIN", 26),
    (207, "Mitchell Robinson", "C", "NYK", 27),
    (208, "Cam Spencer", "G", "MEM", 25),
    (209, "Bub Carrington", "G", "WAS", 20),
    (210, "Noah Penda", "G", "ORL", 21),
    (211, "Taylor Hendricks", "F", "MEM", 22),
    (212, "Tobias Harris", "F", "DET", 33),
    (213, "Alex Caruso", "G", "OKC", 32),
    (214, "Dennis Schröder", "G", "CLE", 32),
    (215, "Tristan da Silva", "F", "ORL", 24),
    (216, "DaRon Holmes II", "F", "DEN", 23),
    (217, "Wendell Carter Jr.", "C", "ORL", 26),
    (218, "Day'Ron Sharpe", "C", "BKN", 24),
    (219, "Rui Hachimura", "F", "LAL", 28),
    (220, "Luguentz Dort", "G", "OKC", 26),
    (221, "Will Richard", "G", "GSW", 23),
    (222, "Jay Huff", "C", "IND", 28),
    (223, "Russell Westbrook", "G", "SAC", 37),
    (224, "Obi Toppin", "F", "IND", 27),
    (225, "Terrence Shannon Jr.", "F", "MIN", 25),
    (226, "Collin Gillespie", "G", "PHX", 26),
    (227, "Miles McBride", "G", "NYK", 25),
    (228, "Naji Marshall", "F", "DAL", 28),
    (229, "Keldon Johnson", "F", "SAS", 26),
    (230, "Devin Carter", "G", "SAC", 23),
    (231, "Ryan Nembhard", "G", "DAL", 22),
    (232, "AJ Green", "G", "MIL", 26),
    (233, "Liam McNeeley", "F", "CHA", 20),
    (234, "Brandon Williams", "G", "DAL", 26),
    (235, "Tre Jones", "G", "CHI", 26),
    (236, "Drake Powell", "G", "BKN", 20),
    (237, "Grayson Allen", "G", "PHX", 30),
    (238, "Asa Newell", "F", "ATL", 20),
    (239, "Sam Hauser", "F", "BOS", 28),
    (240, "T.J. McConnell", "G", "IND", 33),
    (241, "Nolan Traore", "G", "BKN", 19),
    (242, "Saddiq Bey", "G", "NOP", 26),
    (243, "Gradey Dick", "G", "TOR", 22),
    (244, "Kelly Oubre Jr.", "F", "PHI", 30),
    (245, "Rasheer Fleming", "F", "PHX", 21),
    (246, "Bobby Portis", "F", "MIL", 31),
    (247, "Jordan Walsh", "G", "BOS", 21),
    (248, "Kevin Huerter", "G", "DET", 27),
    (249, "Kris Dunn", "G", "LAC", 31),
    (250, "Isaiah Joe", "G", "OKC", 26),
    (251, "Sam Merrill", "G", "CLE", 29),
    (252, "Quinten Post", "C", "GSW", 25),
    (253, "Jarace Walker", "F", "IND", 22),
    (254, "Bruce Brown", "G", "DEN", 29),
    (255, "Yves Missi", "C", "NOP", 21),
    (256, "Cam Whitmore", "F", "WAS", 21),
    (257, "Lonzo Ball", "G", "", 28),
    (258, "Adem Bona", "F", "PHI", 22),
    (259, "Jalen Smith", "C", "CHI", 25),
    (260, "Mouhamed Gueye", "F", "ATL", 23),
    (261, "Brice Sensabaugh", "F", "UTA", 22),
    (262, "Adou Thiero", "G", "LAL", 21),
    (263, "Julian Champagnie", "F", "SAS", 24),
    (264, "Will Riley", "F", "WAS", 20),
    (265, "Vít Krejčí", "F", "POR", 25),
    (266, "Jose Alvarado", "G", "NYK", 27),
    (267, "Tidjane Salaün", "F", "CHA", 20),
    (268, "Duncan Robinson", "F", "DET", 31),
    (269, "Bradley Beal", "G", "LAC", 32),
    (270, "Sandro Mamukelashvili", "C", "TOR", 26),
    (271, "Isaiah Jackson", "F", "LAC", 24),
    (272, "D'Angelo Russell", "G", "WAS", 30),
    (273, "Gary Trent Jr.", "G", "MIL", 27),
    (274, "Bogdan Bogdanović", "G", "LAC", 33),
    (275, "Caris LeVert", "G", "DET", 31),
    (276, "Jonas Valančiūnas", "C", "DEN", 33),
    (277, "Daniss Jenkins", "G", "DET", 24),
    (278, "Kam Jones", "G", "IND", 24),
    (279, "Vince Williams Jr.", "F", "UTA", 25),
    (280, "Ben Saraf", "G", "BKN", 19),
    (281, "Malik Beasley", "G", "DET", 28),
    (282, "De'Anthony Melton", "G", "GSW", 27),
    (283, "Robert Williams III", "C", "POR", 28),
    (284, "Royce O'Neale", "F", "PHX", 32),
    (285, "Derrick Jones Jr.", "F", "LAC", 29),
    (286, "Khris Middleton", "F", "DAL", 34),
    (287, "Corey Kispert", "F", "ATL", 27),
    (288, "Tyler Kolek", "F", "NYK", 24),
    (289, "Jusuf Nurkić", "C", "UTA", 31),
    (290, "Jamal Shead", "G", "TOR", 23),
    (291, "Johnny Furphy", "G", "IND", 21),
    (292, "Terance Mann", "G", "BKN", 29),
    (293, "Guerschon Yabusele", "F", "CHI", 30),
    (294, "Sion James", "G", "CHA", 23),
    (295, "Justin Edwards", "F", "PHI", 22),
    (296, "Tyrese Proctor", "G", "CLE", 21),
    (297, "Trendon Watford", "G", "PHI", 25),
    (298, "Jock Landale", "C", "ATL", 30),
    (299, "Max Strus", "G", "CLE", 29),
    (300, "Cole Anthony", "G", "", 25),
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
    # Build Lawson lookup: normalized_name -> (rank, pos, team, age)
    lawson_lookup = {}
    for rank, name, pos, team, age in LAWSON_RANKINGS:
        key = normalize(name)
        lawson_lookup[key] = (rank, name, pos, team, age)

    # Read master
    with open(MASTER_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)
        rows = list(reader)

    # Insert new column before "Average Rank"
    avg_rank_idx = fieldnames.index("Average Rank")
    new_fieldnames = fieldnames[:avg_rank_idx] + [NEW_COL] + fieldnames[avg_rank_idx:]

    # Track which Lawson players matched
    matched_keys = set()

    # Update existing rows
    for row in rows:
        key = normalize(row["Player"])
        if key in lawson_lookup:
            rank, _, _, _, _ = lawson_lookup[key]
            row[NEW_COL] = rank
            matched_keys.add(key)
        else:
            row[NEW_COL] = ""

    # Find unmatched Lawson players (not in master)
    unmatched = []
    for rank, name, pos, team, age in LAWSON_RANKINGS:
        key = normalize(name)
        if key not in matched_keys:
            unmatched.append((rank, name, pos, team, age))

    print(f"Matched: {len(matched_keys)} players")
    print(f"New players to add: {len(unmatched)}")
    for rank, name, pos, team, age in unmatched:
        print(f"  [{rank}] {name} ({pos}, {team})")

    # Add new rows for unmatched Lawson players
    for rank, name, pos, team, age in unmatched:
        # Determine Level
        nba_teams = {
            "ATL","BKN","BOS","CHA","CHI","CLE","DAL","DEN","DET","GSW",
            "HOU","IND","LAC","LAL","MEM","MIA","MIL","MIN","NOP","NYK",
            "OKC","ORL","PHI","PHX","POR","SAC","SAS","TOR","UTA","WAS",
        }
        team_val = team if team else ""
        level = "NBA" if team_val in nba_teams else "College"
        age_val = str(age) if age else ""

        new_row = {
            "Player": name,
            "Position": pos,
            "Team": team_val,
            "Age": age_val,
            "Level": level,
            "ETA": "",
            "Dizzle Dynasty (Cat, Mar 2026)": "",
            "Noah Rubin (Cat, Jan 2026)": "",
            NEW_COL: rank,
            "Average Rank": "",
            "Rank Variance": "",
        }
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
