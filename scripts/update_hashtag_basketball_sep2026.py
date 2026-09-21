#!/usr/bin/env python3
"""Update Hashtag Basketball rankings: rename from Pts Feb 2026 to Pts Sep 2026 and replace all values."""

import csv
import re
import unicodedata
import subprocess

MASTER_PATH = "basketball/basketball_rankings_master.csv"
OLD_COL = "Hashtag Basketball (Pts, Feb 2026)"
NEW_COL = "Hashtag Basketball (Pts, Sep 2026)"

# Source name (normalized) -> canonical normalized name in master
NAME_MAP = {
    "alexandre sarr":    "alex sarr",
    "carlton carrington": "bub carrington",
    "ron holland":       "ronald holland",
    "nicolas claxton":   "nic claxton",
}

# New Hashtag Basketball (Pts, Sep 2026) rankings.
# "2027 Draft (Pick N)" slots omitted (ranks 40, 47, 56, 94, 123, 196, 232).
HASHTAG_RANKINGS_RAW = [
    (1,   "Victor Wembanyama"),
    (2,   "Shai Gilgeous-Alexander"),
    (3,   "Luka Doncic"),
    (4,   "Nikola Jokic"),
    (5,   "Giannis Antetokounmpo"),
    (6,   "Cade Cunningham"),
    (7,   "Cooper Flagg"),
    (8,   "Anthony Edwards"),
    (9,   "Tyrese Maxey"),
    (10,  "Scottie Barnes"),
    (11,  "Alperen Sengun"),
    (12,  "Cameron Boozer"),
    (13,  "Jalen Johnson"),
    (14,  "Jayson Tatum"),
    (15,  "Tyrese Haliburton"),
    (16,  "Chet Holmgren"),
    (17,  "Evan Mobley"),
    (18,  "Dylan Harper"),
    (19,  "Donovan Mitchell"),
    (20,  "Jalen Williams"),
    (21,  "Darryn Peterson"),
    (22,  "Trey Murphy III"),
    (23,  "Amen Thompson"),
    (24,  "Austin Reaves"),
    (25,  "Trae Young"),
    (26,  "Devin Booker"),
    (27,  "Paolo Banchero"),
    (28,  "Josh Giddey"),
    (29,  "Alexandre Sarr"),
    (30,  "AJ Dybantsa"),
    (31,  "Deni Avdija"),
    (32,  "Karl-Anthony Towns"),
    (33,  "Kon Knueppel"),
    (34,  "Franz Wagner"),
    (35,  "Jamal Murray"),
    (36,  "Jalen Duren"),
    (37,  "Caleb Wilson"),
    (38,  "Jaren Jackson Jr."),
    (39,  "Jalen Brunson"),
    (41,  "LaMelo Ball"),
    (42,  "Zion Williamson"),
    (43,  "Stephon Castle"),
    (44,  "Donovan Clingan"),
    (45,  "Darius Garland"),
    (46,  "Matas Buzelis"),
    (48,  "Brandon Miller"),
    (49,  "Bam Adebayo"),
    (50,  "VJ Edgecombe"),
    (51,  "Jaylen Brown"),
    (52,  "Keyonte George"),
    (53,  "Anthony Davis"),
    (54,  "Tyler Herro"),
    (55,  "De'Aaron Fox"),
    (57,  "Mikel Brown Jr."),
    (58,  "Darius Acuff Jr."),
    (59,  "Keaton Wagler"),
    (60,  "James Harden"),
    (61,  "Stephen Curry"),
    (62,  "RJ Barrett"),
    (63,  "Domantas Sabonis"),
    (64,  "Lauri Markkanen"),
    (65,  "Zach Edey"),
    (66,  "Onyeka Okongwu"),
    (67,  "Pascal Siakam"),
    (68,  "Ivica Zubac"),
    (69,  "Desmond Bane"),
    (70,  "Walker Kessler"),
    (71,  "Nickeil Alexander-Walker"),
    (72,  "Kel'el Ware"),
    (73,  "OG Anunoby"),
    (74,  "Michael Porter Jr."),
    (75,  "Keegan Murray"),
    (76,  "Jalen Green"),
    (77,  "Ja Morant"),
    (78,  "Julius Randle"),
    (79,  "Fred VanVleet"),
    (80,  "Scoot Henderson"),
    (81,  "Derrick White"),
    (82,  "Naz Reid"),
    (83,  "Kevin Durant"),
    (84,  "Jaden McDaniels"),
    (85,  "Brandon Ingram"),
    (86,  "Derik Queen"),
    (87,  "Brayden Burries"),
    (88,  "Kingston Flemings"),
    (89,  "Collin Murray-Boyles"),
    (90,  "Reed Sheppard"),
    (91,  "Immanuel Quickley"),
    (92,  "Dejounte Murray"),
    (93,  "Ajay Mitchell"),
    (95,  "Mikal Bridges"),
    (96,  "Isaiah Hartenstein"),
    (97,  "Anthony Black"),
    (98,  "Kyshawn George"),
    (99,  "Jalen Suggs"),
    (100, "Kyrie Irving"),
    (101, "Jabari Smith Jr."),
    (102, "Nicolas Claxton"),
    (103, "Joel Embiid"),
    (104, "Dyson Daniels"),
    (105, "Day'Ron Sharpe"),
    (106, "Kawhi Leonard"),
    (107, "Coby White"),
    (108, "Myles Turner"),
    (109, "Ace Bailey"),
    (110, "Norman Powell"),
    (111, "Jeremiah Fears"),
    (112, "Morez Johnson Jr."),
    (113, "Jarrett Allen"),
    (114, "Rudy Gobert"),
    (115, "Zach LaVine"),
    (116, "Deandre Ayton"),
    (117, "Kristaps Porzingis"),
    (118, "Mark Williams"),
    (119, "Peyton Watson"),
    (120, "Brandin Podziemski"),
    (121, "Cedric Coward"),
    (122, "Jaime Jaquez Jr."),
    (124, "Devin Vassell"),
    (125, "Ryan Rollins"),
    (126, "Ausar Thompson"),
    (127, "Toumani Camara"),
    (128, "Paul George"),
    (129, "Christian Braun"),
    (130, "Payton Pritchard"),
    (131, "Ayo Dosunmu"),
    (132, "Egor Demin"),
    (133, "Miles Bridges"),
    (134, "Shaedon Sharpe"),
    (135, "Josh Hart"),
    (136, "Maxime Raynaud"),
    (137, "LeBron James"),
    (138, "Cason Wallace"),
    (139, "Allen Graves"),
    (140, "Yaxel Lendeborg"),
    (141, "Ryan Kalkbrenner"),
    (142, "Tre Johnson"),
    (143, "Jakob Poeltl"),
    (144, "Bilal Coulibaly"),
    (145, "Moussa Diabate"),
    (146, "Dereck Lively II"),
    (147, "Andrew Nembhard"),
    (148, "Santi Aldama"),
    (149, "Wendell Carter Jr."),
    (150, "Collin Gillespie"),
    (151, "Andrew Wiggins"),
    (152, "Hannes Steinbach"),
    (153, "Dailyn Swain"),
    (154, "Nate Ament"),
    (155, "Tari Eason"),
    (156, "Cameron Johnson"),
    (157, "Khaman Maluach"),
    (158, "DeMar DeRozan"),
    (159, "Jaylen Wells"),
    (160, "CJ McCollum"),
    (161, "Jimmy Butler"),
    (162, "Anfernee Simons"),
    (163, "Aaron Nesmith"),
    (164, "Isaiah Stewart"),
    (165, "Yanic Konan Niederhauser"),
    (166, "Herbert Jones"),
    (167, "P.J. Washington"),
    (168, "Bennedict Mathurin"),
    (169, "Oso Ighodaro"),
    (170, "Daniss Jenkins"),
    (171, "Robert Williams III"),
    (172, "Kevin Porter Jr."),
    (173, "Jaylon Tyson"),
    (174, "Zaccharie Risacher"),
    (175, "Aaron Gordon"),
    (176, "Davion Mitchell"),
    (177, "Damian Lillard"),
    (178, "Joan Beringer"),
    (179, "Dillon Brooks"),
    (180, "Daniel Gafford"),
    (181, "Aday Mara"),
    (182, "Ty Jerome"),
    (183, "Grayson Allen"),
    (184, "Terrence Shannon Jr."),
    (185, "Malik Monk"),
    (186, "Jonathan Kuminga"),
    (187, "Ebuka Okorie"),
    (188, "Christian Anderson"),
    (189, "Joshua Jefferson"),
    (190, "Jarace Walker"),
    (191, "John Collins"),
    (192, "Neemias Queta"),
    (193, "Kyle Filipowski"),
    (194, "Gui Santos"),
    (195, "Isaiah Collier"),
    (197, "Jordan Poole"),
    (198, "Rui Hachimura"),
    (199, "Jared McCain"),
    (200, "Carlton Carrington"),
    (201, "Will Riley"),
    (202, "Max Christie"),
    (203, "Caris LeVert"),
    (204, "Nique Clifford"),
    (205, "Noah Clowney"),
    (206, "Collin Sexton"),
    (207, "Carter Bryant"),
    (208, "Rasheer Fleming"),
    (209, "Saddiq Bey"),
    (210, "Jaylin Williams"),
    (211, "Mitchell Robinson"),
    (212, "Leonard Miller"),
    (213, "Max Strus"),
    (214, "Jalen Smith"),
    (215, "Donte DiVincenzo"),
    (216, "Nikola Jovic"),
    (217, "Ron Holland II"),
    (218, "Cam Spencer"),
    (219, "Cam Whitmore"),
    (220, "Kasparas Jakucionis"),
    (221, "De'Andre Hunter"),
    (222, "Tobias Harris"),
    (223, "Obi Toppin"),
    (224, "Cameron Carr"),
    (225, "Jerami Grant"),
    (226, "Ousmane Dieng"),
    (227, "Dylan Cardwell"),
    (228, "Naji Marshall"),
    (229, "Labaron Philon Jr."),
    (230, "Jusuf Nurkic"),
    (231, "Sandro Mamukelashvili"),
    (233, "Nikola Vucevic"),
    (234, "Zuby Ejiofor"),
    (235, "Karim Lopez"),
    (236, "Jayden Quaintance"),
    (237, "Jay Huff"),
    (238, "Jamal Shead"),
    (239, "Dru Smith"),
    (240, "Isaiah Jackson"),
    (241, "Keon Ellis"),
    (242, "Thomas Sorber"),
    (243, "De'Anthony Melton"),
    (244, "Jrue Holiday"),
    (245, "Hugo Gonzalez"),
    (246, "Drake Powell"),
    (247, "Brice Sensabaugh"),
    (248, "Taylor Hendricks"),
    (249, "Yang Hansen"),
    (250, "Kelly Oubre Jr."),
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
    hashtag_lookup = {}
    for rank, name in HASHTAG_RANKINGS_RAW:
        key = normalize(name)
        mapped_key = NAME_MAP.get(key, key)
        hashtag_lookup[mapped_key] = (rank, name)

    with open(MASTER_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        old_fieldnames = list(reader.fieldnames)
        rows = list(reader)

    new_fieldnames = [NEW_COL if fn == OLD_COL else fn for fn in old_fieldnames]

    matched_keys = set()
    for row in rows:
        row[NEW_COL] = row.pop(OLD_COL, "")
        key = normalize(row["Player"])
        if key in hashtag_lookup:
            rank, _ = hashtag_lookup[key]
            row[NEW_COL] = rank
            matched_keys.add(key)
        else:
            row[NEW_COL] = ""

    unmatched = []
    for rank, name in HASHTAG_RANKINGS_RAW:
        key = normalize(name)
        mapped_key = NAME_MAP.get(key, key)
        if mapped_key not in matched_keys:
            unmatched.append((rank, name))

    print(f"Matched: {len(matched_keys)} players")
    print(f"New players to add: {len(unmatched)}")
    for rank, name in unmatched:
        print(f"  [{rank}] {name}")

    nba_teams = {
        "ATL","BKN","BOS","CHA","CHI","CLE","DAL","DEN","DET","GSW",
        "HOU","IND","LAC","LAL","MEM","MIA","MIL","MIN","NOP","NYK",
        "OKC","ORL","PHI","PHX","POR","SAC","SAS","TOR","UTA","WAS",
    }

    for rank, name in unmatched:
        new_row = {fn: "" for fn in new_fieldnames}
        new_row["Player"] = name
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
