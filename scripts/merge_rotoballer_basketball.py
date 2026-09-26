#!/usr/bin/env python3
"""Merge RotoBaller (Pts, Sep 2026) basketball rankings into the master CSV."""

import csv
import re
import unicodedata
import subprocess

MASTER_PATH = "basketball/basketball_rankings_master.csv"
NEW_COL = "RotoBaller (Pts, Sep 2026)"

# Raw (rank, name) pairs as published by RotoBaller
ROTOBALLER_RANKINGS = [
    (1, "Victor Wembanyama"), (2, "Shai Gilgeous-Alexander"), (3, "Luka Doncic"),
    (4, "Nikola Jokic"), (5, "Cooper Flagg"), (6, "Cade Cunningham"),
    (7, "Jayson Tatum"), (8, "Anthony Edwards"), (9, "Jalen Johnson"),
    (10, "Tyrese Maxey"), (11, "Cameron Boozer"), (12, "Scottie Barnes"),
    (13, "Tyrese Haliburton"), (14, "Alperen Sengun"), (15, "AJ Dybantsa"),
    (16, "Giannis Antetokounmpo"), (17, "Darryn Peterson"), (18, "Amen Thompson"),
    (19, "Evan Mobley"), (20, "Dylan Harper"), (21, "Jalen Williams"),
    (22, "Kon Knueppel"), (23, "Paolo Banchero"), (24, "Josh Giddey"),
    (25, "Donovan Mitchell"), (26, "Deni Avdija"), (27, "Chet Holmgren"),
    (28, "Franz Wagner"), (29, "Austin Reaves"), (30, "Caleb Wilson"),
    (31, "Jamal Murray"), (32, "Darius Garland"), (33, "Jalen Brunson"),
    (34, "LaMelo Ball"), (35, "Jalen Duren"), (36, "Devin Booker"),
    (37, "Karl-Anthony Towns"), (38, "Trey Murphy III"), (39, "Jaylen Brown"),
    (40, "Trae Young"), (41, "Stephon Castle"), (42, "Brandon Miller"),
    (43, "Bam Adebayo"), (44, "VJ Edgecombe"), (45, "Lauri Markkanen"),
    (46, "Donovan Clingan"), (47, "Walker Kessler"), (48, "Alex Sarr"),
    (49, "Keyonte George"), (50, "Darius Acuff Jr."), (51, "Zach Edey"),
    (52, "Brandon Ingram"), (53, "Jaren Jackson Jr."), (54, "Keaton Wagler"),
    (55, "Domantas Sabonis"), (56, "Onyeka Okongwu"), (57, "Desmond Bane"),
    (58, "Kevin Durant"), (59, "James Harden"), (60, "Mikel Brown Jr."),
    (61, "De'Aaron Fox"), (62, "Zion Williamson"), (63, "Stephen Curry"),
    (64, "Anthony Davis"), (65, "Collin Murray-Boyles"), (66, "Kel'el Ware"),
    (67, "Ivica Zubac"), (68, "Kawhi Leonard"), (69, "Kingston Flemings"),
    (70, "Kyrie Irving"), (71, "Pascal Siakam"), (72, "Matas Buzelis"),
    (73, "OG Anunoby"), (74, "Derrick White"), (75, "Tyler Herro"),
    (76, "Joel Embiid"), (77, "Ja Morant"), (78, "Dyson Daniels"),
    (79, "Ausar Thompson"), (80, "Jalen Suggs"), (81, "Cedric Coward"),
    (82, "Ryan Rollins"), (83, "Nickeil Alexander-Walker"), (84, "Jarrett Allen"),
    (85, "Kyshawn George"), (86, "Derik Queen"), (87, "Jaden McDaniels"),
    (88, "Reed Sheppard"), (89, "Payton Pritchard"), (90, "Ace Bailey"),
    (91, "Isaiah Hartenstein"), (92, "Michael Porter Jr."), (93, "Coby White"),
    (94, "Scoot Henderson"), (95, "Brayden Burries"), (96, "Immanuel Quickley"),
    (97, "Julius Randle"), (98, "Mikal Bridges"), (99, "Yaxel Lendeborg"),
    (100, "Nic Claxton"), (101, "Aday Mara"), (102, "Morez Johnson Jr."),
    (103, "Jalen Green"), (104, "Peyton Watson"), (105, "Naz Reid"),
    (106, "Dejounte Murray"), (107, "Tari Eason"), (108, "Ajay Mitchell"),
    (109, "Anthony Black"), (110, "Zach LaVine"), (111, "Jeremiah Fears"),
    (112, "Egor Demin"), (113, "Miles Bridges"), (114, "Mark Williams"),
    (115, "Keegan Murray"), (116, "Josh Hart"), (117, "Andrew Nembhard"),
    (118, "Tre Johnson"), (119, "Ebuka Okorie"), (120, "Joan Beringer"),
    (121, "Devin Vassell"), (122, "RJ Barrett"), (123, "Khaman Maluach"),
    (124, "Day'Ron Sharpe"), (125, "Hannes Steinbach"), (126, "Paul George"),
    (127, "Toumani Camara"), (128, "Norman Powell"), (129, "Myles Turner"),
    (130, "Cason Wallace"), (131, "PJ Washington"), (132, "Jabari Smith Jr."),
    (133, "Jakob Poeltl"), (134, "Fred VanVleet"), (135, "Shaedon Sharpe"),
    (136, "Ty Jerome"), (137, "Rudy Gobert"), (138, "Kristaps Porzingis"),
    (139, "Bennett Stirtz"), (140, "Santi Aldama"), (141, "Aaron Gordon"),
    (142, "Neemias Queta"), (143, "Jared McCain"), (144, "Dailyn Swain"),
    (145, "Cameron Carr"), (146, "John Collins"), (147, "Jaime Jaquez Jr."),
    (148, "Bilal Coulibaly"), (149, "Dereck Lively II"), (150, "Ronald Holland II"),
    (151, "Maxime Raynaud"), (152, "LeBron James"), (153, "Christian Anderson"),
    (154, "Thomas Sorber"), (155, "Carter Bryant"), (156, "Ayo Dosunmu"),
    (157, "Naji Marshall"), (158, "Damian Lillard"), (159, "Andrew Wiggins"),
    (160, "Christian Braun"), (161, "Labaron Philon"), (162, "Nate Ament"),
    (163, "Brandin Podziemski"), (164, "Jaylon Tyson"), (165, "Quentin Grimes"),
    (166, "Will Riley"), (167, "Kevin Porter Jr."), (168, "Deandre Ayton"),
    (169, "Daniel Gafford"), (170, "Moussa Diabate"), (171, "Aaron Nesmith"),
    (172, "Kasparas Jakucionis"), (173, "Collin Gillespie"), (174, "Julian Champagnie"),
    (175, "Wendell Carter Jr."), (176, "Jonathan Kuminga"), (177, "Kyle Filipowski"),
    (178, "Isaiah Stewart"), (179, "Dillon Brooks"), (180, "Davion Mitchell"),
    (181, "Jimmy Butler"), (182, "Cameron Johnson"), (183, "CJ McCollum"),
    (184, "Hugo Gonzalez"), (185, "Karim Lopez"), (186, "Tarris Reed Jr."),
    (187, "Allen Graves"), (188, "Gui Santos"), (189, "Noa Essengue"),
    (190, "Grayson Allen"), (191, "Malik Monk"), (192, "Herbert Jones"),
    (193, "Max Christie"), (194, "Rui Hachimura"), (195, "Draymond Green"),
    (196, "Bennedict Mathurin"), (197, "Paul Reed"), (198, "Anfernee Simons"),
    (199, "Nique Clifford"), (200, "Danny Wolf"), (201, "Mitchell Robinson"),
    (202, "Daniss Jenkins"), (203, "Cam Spencer"), (204, "Jrue Holiday"),
    (205, "Jamal Shead"), (206, "Bruce Thornton"), (207, "DeMar DeRozan"),
    (208, "Scotty Pippen Jr."), (209, "Jordan Poole"), (210, "Josh Minott"),
    (211, "De'Andre Hunter"), (212, "Aaron Wiggins"), (213, "Nikola Topic"),
    (214, "Tre Jones"), (215, "Jusuf Nurkic"), (216, "Walter Clayton Jr."),
    (217, "Bobby Portis"), (218, "Sam Hauser"), (219, "Saddiq Bey"),
    (220, "Sandro Mamukelashvili"), (221, "Isaiah Collier"), (222, "Robert Williams III"),
    (223, "Tobias Harris"), (224, "Nikola Vucevic"), (225, "Nolan Traore"),
    (226, "Sergio De Larrea"), (227, "Zuby Ejiofor"), (228, "Kobe Sanders"),
    (229, "De'Anthony Melton"), (230, "Jerami Grant"), (231, "Jaylen Wells"),
    (232, "Ousmane Dieng"), (233, "Terrence Shannon Jr."), (234, "Sam Merrill"),
    (235, "Zaccharie Risacher"), (236, "Koa Peat"), (237, "Meleek Thomas"),
    (238, "Ryan Kalkbrenner"), (239, "Tristan Da Silva"), (240, "Chris Cenac Jr."),
    (241, "Keldon Johnson"), (242, "Dylan Cardwell"), (243, "Yanic Konan Niederhauser"),
    (244, "Kelly Oubre Jr."), (245, "Brice Sensabaugh"), (246, "Taylor Hendricks"),
    (247, "Ryan Nembhard"), (248, "GG Jackson"), (249, "Rasheer Fleming"),
    (250, "Luguentz Dort"), (251, "Rob Dillingham"), (252, "Joshua Jefferson"),
    (253, "Jayden Quaintance"), (254, "Isaiah Evans"), (255, "Richie Saunders"),
    (256, "Miles McBride"), (257, "Donte DiVincenzo"), (258, "Quentin Post"),
    (259, "Yang Hansen"), (260, "Pelle Larsson"), (261, "Kyle Kuzma"),
    (262, "Baylor Scheierman"), (263, "Max Strus"), (264, "Bradley Beal"),
    (265, "Moses Moody"), (266, "Noah Clowney"), (267, "Jase Richardson"),
    (268, "Collin Sexton"), (269, "Royce O'Neale"), (270, "Alex Karaban"),
    (271, "Jay Huff"), (272, "Justin Champagnie"), (273, "Jalen Smith"),
    (274, "Ryan Conwell"), (275, "Oso Ighodaro"), (276, "Henri Veesaar"),
    (277, "Baba Miller"), (278, "Dennis Schroder"), (279, "Asa Newell"),
    (280, "Noah Penda"), (281, "Jose Alvarado"), (282, "Javon Small"),
    (283, "Luke Kennard"), (284, "Adem Bona"), (285, "Tidjane Salaun"),
    (286, "Bogoljbub Markovic"), (287, "Ja'Kobe Walter"), (288, "Kris Dunn"),
    (289, "Jordan Walsh"), (290, "Obi Toppin"), (291, "Emanuel Sharp"),
    (292, "Bub Carrington"), (293, "TJ McConnell"), (294, "Derrick Jones Jr."),
    (295, "Dean Wade"), (296, "Nikola Jovic"), (297, "Adou Thiero"),
    (298, "Jordan Miller"), (299, "Duncan Robinson"), (300, "Tim Hardaway Jr."),
]

# Corrections to canonical master spelling for names that don't normalize-match
# due to typos or the project's preferred canonical form (see CLAUDE.md).
NAME_MAP = {
    "Ron Holland": "Ronald Holland II",
    "Carlton Carrington": "Bub Carrington",
}


def normalize(name):
    name = unicodedata.normalize("NFKD", name)
    name = name.encode("ascii", "ignore").decode("ascii")
    name = name.lower()
    name = re.sub(r"\b(jr|sr|ii|iii|iv|v)\b\.?", "", name)
    name = re.sub(r"[^a-z\s]", "", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name


def main():
    roto_lookup = {}
    for rank, name in ROTOBALLER_RANKINGS:
        canonical = NAME_MAP.get(name, name)
        key = normalize(canonical)
        roto_lookup[key] = (rank, canonical)

    with open(MASTER_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)
        rows = list(reader)

    avg_rank_idx = fieldnames.index("Average Rank")
    new_fieldnames = fieldnames[:avg_rank_idx] + [NEW_COL] + fieldnames[avg_rank_idx:]

    matched_keys = set()

    for row in rows:
        key = normalize(row["Player"])
        if key in roto_lookup:
            rank, _ = roto_lookup[key]
            row[NEW_COL] = rank
            matched_keys.add(key)
        else:
            row[NEW_COL] = ""

    unmatched = []
    for key, (rank, canonical) in roto_lookup.items():
        if key not in matched_keys:
            unmatched.append((rank, canonical))
    unmatched.sort()

    print(f"Matched: {len(matched_keys)} players")
    print(f"New players to add: {len(unmatched)}")
    for rank, name in unmatched:
        print(f"  [{rank}] {name}")

    for rank, name in unmatched:
        new_row = {col: "" for col in new_fieldnames}
        new_row["Player"] = name
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
