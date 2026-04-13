#!/usr/bin/env python3
"""Update Dizzle Dynasty basketball rankings: rename from Cat Mar 2026 to Pts Apr 2026 and replace all values."""

import csv
import re
import unicodedata
import subprocess

MASTER_PATH = "basketball/basketball_rankings_master.csv"
OLD_COL = "Dizzle Dynasty (Cat, Mar 2026)"
NEW_COL = "Dizzle Dynasty (Pts, Apr 2026)"

# Source name (normalized) -> canonical normalized name in master
# Used where normalization alone doesn't resolve the mismatch
NAME_MAP = {
    "carlton carrington": "bub carrington",       # canonical is Bub Carrington
    "ron holland":        "ronald holland",         # canonical is Ronald Holland II (II stripped by normalize)
    "khaman malauch":     "khaman maluach",         # spelling variant in source
    "ayo dosumnu":        "ayo dosunmu",            # spelling variant in source
}

# New Dizzle Dynasty (Pts, Apr 2026) rankings — 250 players
# Draft picks provided as "X.YY / Player Name"; player name is extracted automatically.
DIZZLE_RANKINGS_RAW = [
    (1,   "Victor Wembanyama"),
    (2,   "Luka Doncic"),
    (3,   "Shai Gilgeous-Alexander"),
    (4,   "Nikola Jokic"),
    (5,   "Cade Cunningham"),
    (6,   "Cooper Flagg"),
    (7,   "Tyrese Maxey"),
    (8,   "Jalen Johnson"),
    (9,   "Anthony Edwards"),
    (10,  "Jayson Tatum"),
    (11,  "Alperen Sengun"),
    (12,  "Giannis Antetokounmpo"),
    (13,  "Tyrese Haliburton"),
    (14,  "1.01 / Cameron Boozer"),
    (15,  "Scottie Barnes"),
    (16,  "1.02 / Darryn Peterson"),
    (17,  "Amen Thompson"),
    (18,  "Deni Avdija"),
    (19,  "Evan Mobley"),
    (20,  "1.03 / AJ Dybantsa"),
    (21,  "LaMelo Ball"),
    (22,  "Paolo Banchero"),
    (23,  "Josh Giddey"),
    (24,  "Austin Reaves"),
    (25,  "Donovan Mitchell"),
    (26,  "Jalen Williams"),
    (27,  "Franz Wagner"),
    (28,  "Chet Holmgren"),
    (29,  "Dylan Harper"),
    (30,  "Devin Booker"),
    (31,  "Trae Young"),
    (32,  "Jalen Duren"),
    (33,  "Darius Garland"),
    (34,  "Kon Knueppel"),
    (35,  "Jamal Murray"),
    (36,  "Jaylen Brown"),
    (37,  "Trey Murphy III"),
    (38,  "1.04 / Caleb Wilson"),
    (39,  "VJ Edgecombe"),
    (40,  "Jalen Brunson"),
    (41,  "Donovan Clingan"),
    (42,  "Karl-Anthony Towns"),
    (43,  "Alex Sarr"),
    (44,  "Keyonte George"),
    (45,  "Bam Adebayo"),
    (46,  "James Harden"),
    (47,  "Stephon Castle"),
    (48,  "1.05 / Kingston Flemings"),
    (49,  "Lauri Markkanen"),
    (50,  "Domantas Sabonis"),
    (51,  "Kevin Durant"),
    (52,  "De'Aaron Fox"),
    (53,  "Brandon Miller"),
    (54,  "Zach Edey"),
    (55,  "Ace Bailey"),
    (56,  "Onyeka Okongwu"),
    (57,  "Tyler Herro"),
    (58,  "Desmond Bane"),
    (59,  "Ivica Zubac"),
    (60,  "Derik Queen"),
    (61,  "Jaren Jackson Jr."),
    (62,  "Anthony Davis"),
    (63,  "1.06 / Keaton Wagler"),
    (64,  "Zion Williamson"),
    (65,  "Kyrie Irving"),
    (66,  "Stephen Curry"),
    (67,  "Ja Morant"),
    (68,  "1.07 / Mikel Brown Jr."),
    (69,  "1.08 / Darius Acuff Jr."),
    (70,  "Joel Embiid"),
    (71,  "Walker Kessler"),
    (72,  "Kawhi Leonard"),
    (73,  "Pascal Siakam"),
    (74,  "Matas Buzelis"),
    (75,  "Kel'el Ware"),
    (76,  "Dyson Daniels"),
    (77,  "Reed Sheppard"),
    (78,  "Derrick White"),
    (79,  "Julius Randle"),
    (80,  "Brandon Ingram"),
    (81,  "Michael Porter Jr."),
    (82,  "Kyshawn George"),
    (83,  "OG Anunoby"),
    (84,  "Jalen Suggs"),
    (85,  "Ryan Rollins"),
    (86,  "Cedric Coward"),
    (87,  "Isaiah Hartenstein"),
    (88,  "Jarrett Allen"),
    (89,  "Collin Murray-Boyles"),
    (90,  "1.09 / Aday Mara"),
    (91,  "Immanuel Quickley"),
    (92,  "Shaedon Sharpe"),
    (93,  "Mikal Bridges"),
    (94,  "Peyton Watson"),
    (95,  "Mark Williams"),
    (96,  "Ausar Thompson"),
    (97,  "Nickeil Alexander-Walker"),
    (98,  "Zach LaVine"),
    (99,  "Dejounte Murray"),
    (100, "Anthony Black"),
    (101, "1.10 / Jayden Quaintance"),
    (102, "Jeremiah Fears"),
    (103, "Tre Johnson"),
    (104, "Jaden McDaniels"),
    (105, "Tari Eason"),
    (106, "Payton Pritchard"),
    (107, "Scoot Henderson"),
    (108, "Nic Claxton"),
    (109, "1.11 / Brayden Burries"),
    (110, "Jalen Green"),
    (111, "Naz Reid"),
    (112, "RJ Barrett"),
    (113, "Devin Vassell"),
    (114, "Coby White"),
    (115, "1.12 / Dailyn Swain"),
    (116, "Ajay Mitchell"),
    (117, "Egor Demin"),
    (118, "Josh Hart"),
    (119, "Norman Powell"),
    (120, "Andrew Nembhard"),
    (121, "Jabari Smith Jr."),
    (122, "Jonathan Kuminga"),
    (123, "1.13 / Yaxel Lendeborg"),
    (124, "Jaime Jaquez Jr."),
    (125, "Keegan Murray"),
    (126, "Jakob Poeltl"),
    (127, "Myles Turner"),
    (128, "Ty Jerome"),
    (129, "Will Riley"),
    (130, "1.14 / Patrick Ngongba II"),
    (131, "Kevin Porter Jr."),
    (132, "Santi Aldama"),
    (133, "Brandin Podziemski"),
    (134, "Rudy Gobert"),
    (135, "Kristaps Porzingis"),
    (136, "Jared McCain"),
    (137, "De'Andre Ayton"),
    (138, "Miles Bridges"),
    (139, "PJ Washington"),
    (140, "Bilal Coulibaly"),
    (141, "Toumani Camara"),
    (142, "Dereck Lively II"),
    (143, "Jaylon Tyson"),
    (144, "1.15 / Labaron Philon"),
    (145, "Khaman Malauch"),
    (146, "Cason Wallace"),
    (147, "Bennedict Mathurin"),
    (148, "LeBron James"),
    (149, "Christian Braun"),
    (150, "Isaiah Collier"),
    (151, "Nikola Topic"),
    (152, "1.16 / Nate Ament"),
    (153, "Brice Sensabaugh"),
    (154, "Aaron Nesmith"),
    (155, "Aaron Gordon"),
    (156, "Maxime Raynaud"),
    (157, "Neemias Queta"),
    (158, "John Collins"),
    (159, "Moussa Diabate"),
    (160, "Kyle Filipowski"),
    (161, "Jordan Poole"),
    (162, "Malik Monk"),
    (163, "Wendell Carter Jr."),
    (164, "Daniel Gafford"),
    (165, "Quentin Grimes"),
    (166, "Thomas Sorber"),
    (167, "CJ McCollum"),
    (168, "Fred VanVleet"),
    (169, "Ron Holland"),
    (170, "Max Christie"),
    (171, "Jrue Holiday"),
    (172, "Damian Lillard"),
    (173, "Donte DiVincenzo"),
    (174, "Paul George"),
    (175, "Andrew Wiggins"),
    (176, "Naji Marshall"),
    (177, "DeMar DeRozan"),
    (178, "Dillon Brooks"),
    (179, "Walter Clayton Jr."),
    (180, "Saddiq Bey"),
    (181, "Cameron Johnson"),
    (182, "Ryan Kalkbrenner"),
    (183, "Noa Essengue"),
    (184, "Ayo Dosumnu"),
    (185, "Danny Wolf"),
    (186, "Grayson Allen"),
    (187, "Nique Clifford"),
    (188, "Jerami Grant"),
    (189, "Kasparas Jakucionis"),
    (190, "Scotty Pippen Jr."),
    (191, "Daniss Jenkins"),
    (192, "Collin Gillespie"),
    (193, "Draymond Green"),
    (194, "Joan Beringer"),
    (195, "Keldon Johnson"),
    (196, "Tobias Harris"),
    (197, "Anfernee Simons"),
    (198, "Davion Mitchell"),
    (199, "Jimmy Butler"),
    (200, "Zaccharie Risacher"),
    (201, "Josh Minott"),
    (202, "Tristan Da Silva"),
    (203, "Day'Ron Sharpe"),
    (204, "Yang Hansen"),
    (205, "GG Jackson"),
    (206, "Nikola Vucevic"),
    (207, "Herbert Jones"),
    (208, "Cam Spencer"),
    (209, "Ousmane Dieng"),
    (210, "Jase Richardson"),
    (211, "Kyle Kuzma"),
    (212, "Isaiah Stewart"),
    (213, "Noah Clowney"),
    (214, "De'Anthony Melton"),
    (215, "Rui Hachimura"),
    (216, "Isaiah Joe"),
    (217, "De'Andre Hunter"),
    (218, "Jaylen Wells"),
    (219, "Bobby Portis"),
    (220, "Rob Dillingham"),
    (221, "Julian Champagnie"),
    (222, "Nolan Traore"),
    (223, "Collin Sexton"),
    (224, "Sam Hauser"),
    (225, "Russell Westbrook"),
    (226, "Mitchell Robinson"),
    (227, "Brandon Williams"),
    (228, "Kelly Oubre Jr."),
    (229, "Jarace Walker"),
    (230, "Taylor Hendricks"),
    (231, "Keon Ellis"),
    (232, "Carter Bryant"),
    (233, "Sam Merrill"),
    (234, "Luguentz Dort"),
    (235, "Jay Huff"),
    (236, "AJ Green"),
    (237, "Justin Champagnie"),
    (238, "Noah Penda"),
    (239, "Dylan Cardwell"),
    (240, "Dennis Schroder"),
    (241, "Miles McBride"),
    (242, "Hugo Gonzalez"),
    (243, "Devin Carter"),
    (244, "Carlton Carrington"),
    (245, "Duncan Robinson"),
    (246, "Goga Bitadze"),
    (247, "Jordan Walsh"),
    (248, "Adou Thiero"),
    (249, "Jalen Smith"),
    (250, "Luke Kornet"),
]


def normalize(name):
    name = unicodedata.normalize("NFKD", name)
    name = name.encode("ascii", "ignore").decode("ascii")
    name = name.lower()
    name = re.sub(r"\b(jr|sr|ii|iii|iv|v)\b\.?", "", name)
    name = re.sub(r"[^a-z\s]", "", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name


def parse_player_name(raw):
    """Extract player name from draft-pick format '1.01 / Player Name', or return as-is."""
    if " / " in raw:
        return raw.split(" / ", 1)[1].strip()
    return raw.strip()


def main():
    # Build lookup: normalized_name -> (rank, display_name)
    dizzle_lookup = {}
    for rank, raw in DIZZLE_RANKINGS_RAW:
        display = parse_player_name(raw)
        key = normalize(display)
        mapped_key = NAME_MAP.get(key, key)
        dizzle_lookup[mapped_key] = (rank, display)

    with open(MASTER_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        old_fieldnames = list(reader.fieldnames)
        rows = list(reader)

    # Rename the column in fieldnames
    new_fieldnames = [NEW_COL if fn == OLD_COL else fn for fn in old_fieldnames]

    # Clear old Dizzle values and set new ones
    matched_keys = set()
    for row in rows:
        row[NEW_COL] = row.pop(OLD_COL, "")  # rename key in row dict, clear value below
        key = normalize(row["Player"])
        if key in dizzle_lookup:
            rank, _ = dizzle_lookup[key]
            row[NEW_COL] = rank
            matched_keys.add(key)
        else:
            row[NEW_COL] = ""

    # Find unmatched new players (not yet in master)
    unmatched = []
    for rank, raw in DIZZLE_RANKINGS_RAW:
        display = parse_player_name(raw)
        key = normalize(display)
        mapped_key = NAME_MAP.get(key, key)
        if mapped_key not in matched_keys:
            unmatched.append((rank, display))

    print(f"Matched: {len(matched_keys)} players")
    print(f"New players to add: {len(unmatched)}")
    for rank, name in unmatched:
        print(f"  [{rank}] {name}")

    # Append new players (all college draft prospects)
    for rank, name in unmatched:
        new_row = {fn: "" for fn in new_fieldnames}
        new_row["Player"] = name
        new_row["Position"] = ""
        new_row["Team"] = ""
        new_row["Age"] = ""
        new_row["Level"] = "College"
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
