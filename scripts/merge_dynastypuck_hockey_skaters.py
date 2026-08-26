#!/usr/bin/env python3
"""
Merge Dynasty Puck (Aug 2026) skater rankings into hockey_skaters_master.csv.
This is a new source: goalies are excluded here (see merge_dynastypuck_hockey_goalies.py).
Skaters are re-ranked sequentially 1-N among skaters only, by order of appearance
in the original combined 300-player list.
Run recalculate.py afterward.
"""

import csv
import os
import re
import subprocess
import unicodedata

MASTER_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "hockey", "hockey_skaters_master.csv"))
SOURCE_COL = "Dynasty Puck (Aug 2026)"

# (sequential_rank, canonical_name, position)
SKATER_DATA = [
    (1, "Connor McDavid", "F"),
    (2, "Macklin Celebrini", "F"),
    (3, "Nathan MacKinnon", "F"),
    (4, "Cale Makar", "D"),
    (5, "Matthew Schaefer", "D"),
    (6, "Quinn Hughes", "D"),
    (7, "Leon Draisaitl", "F"),
    (8, "Connor Bedard", "F"),
    (9, "Lane Hutson", "D"),
    (10, "Jack Hughes", "F"),
    (11, "Jake Sanderson", "D"),
    (12, "Rasmus Dahlin", "D"),
    (13, "Jason Robertson", "F"),
    (14, "Kirill Kaprizov", "F"),
    (15, "Nick Suzuki", "F"),
    (16, "Leo Carlsson", "F"),
    (17, "Wyatt Johnston", "F"),
    (18, "Zach Werenski", "D"),
    (19, "Nikita Kucherov", "F"),
    (20, "Auston Matthews", "F"),
    (21, "Evan Bouchard", "D"),
    (22, "David Pastrnak", "F"),
    (23, "Jack Eichel", "F"),
    (24, "Moritz Seider", "D"),
    (25, "Tim Stutzle", "F"),
    (26, "Adam Fox", "D"),
    (27, "Ivan Demidov", "F"),
    (28, "Cole Caufield", "F"),
    (29, "Cutter Gauthier", "F"),
    (30, "Miro Heiskanen", "D"),
    (31, "Tage Thompson", "F"),
    (32, "Mikko Rantanen", "F"),
    (33, "Mitch Marner", "F"),
    (34, "Martin Necas", "F"),
    (35, "Gavin McKenna", "F"),
    (36, "Cole Hutson", "D"),
    (37, "Brady Tkachuk", "F"),
    (38, "Juraj Slafkovsky", "F"),
    (39, "Jackson LaCombe", "D"),
    (40, "Matt Boldy", "F"),
    (41, "Dylan Guenther", "F"),
    (42, "Adam Fantilli", "F"),
    (43, "Jakob Chychrun", "D"),
    (44, "Charlie McAvoy", "D"),
    (45, "Kyle Connor", "F"),
    (46, "Logan Cooley", "F"),
    (47, "Brandt Clarke", "D"),
    (48, "Thomas Harley", "D"),
    (49, "Sebastian Aho", "F"),
    (50, "Brock Faber", "D"),
    (51, "Noah Dobson", "D"),
    (52, "Porter Martone", "F"),
    (53, "Mikhail Sergachev", "D"),
    (54, "Beckett Sennecke", "F"),
    (55, "Seth Jarvis", "F"),
    (56, "Luke Hughes", "D"),
    (57, "Bowen Byram", "D"),
    (58, "Lucas Raymond", "F"),
    (59, "Josh Morrissey", "D"),
    (60, "Matthew Tkachuk", "F"),
    (61, "Ivar Stenberg", "F"),
    (62, "William Nylander", "F"),
    (63, "Sam Reinhart", "F"),
    (64, "Clayton Keller", "F"),
    (65, "Nico Hischier", "F"),
    (66, "Pavel Dorofeyev", "F"),
    (67, "Will Smith", "F"),
    (68, "Darren Raddysh", "D"),
    (69, "Dylan Larkin", "F"),
    (70, "Robert Thomas", "F"),
    (71, "Aleksander Barkov", "F"),
    (72, "Mark Scheifele", "F"),
    (73, "Sidney Crosby", "F"),
    (74, "Michael Misa", "F"),
    (75, "Alex DeBrincat", "F"),
    (76, "Jake Guentzel", "F"),
    (77, "Brayden Point", "F"),
    (78, "Andrei Svechnikov", "F"),
    (79, "Dylan Holloway", "F"),
    (80, "Elias Pettersson", "F"),
    (81, "Matvei Michkov", "F"),
    (82, "Brandon Hagel", "F"),
    (83, "Anton Frondell", "F"),
    (84, "Thomas Chabot", "D"),
    (85, "Roman Josi", "D"),
    (86, "Kirill Marchenko", "F"),
    (87, "Matthew Knies", "F"),
    (88, "Mathew Barzal", "F"),
    (89, "Jimmy Snuggerud", "F"),
    (90, "Filip Forsberg", "F"),
    (91, "Trevor Zegras", "F"),
    (92, "Zayne Parekh", "D"),
    (93, "Logan Stankoven", "F"),
    (94, "Ryan Leonard", "F"),
    (95, "Erik Karlsson", "D"),
    (96, "Dylan Cozens", "F"),
    (97, "Jesper Bratt", "F"),
    (98, "Zeev Buium", "D"),
    (99, "Adrian Kempe", "F"),
    (100, "Quinton Byfield", "F"),
    (101, "Alex Tuch", "F"),
    (102, "Alexander Nikishin", "D"),
    (103, "Zach Benson", "F"),
    (104, "Jordan Kyrou", "F"),
    (105, "Bo Horvat", "F"),
    (106, "Chase Reid", "D"),
    (107, "Simon Edvinsson", "D"),
    (108, "William Eklund", "F"),
    (109, "Owen Power", "D"),
    (110, "Seth Jones", "D"),
    (111, "Roope Hintz", "F"),
    (112, "Drake Batherson", "F"),
    (113, "Joel Eriksson Ek", "F"),
    (114, "Artemi Panarin", "F"),
    (115, "Gabriel Vilardi", "F"),
    (116, "Travis Konecny", "F"),
    (117, "Nick Schmaltz", "F"),
    (118, "James Hagens", "F"),
    (119, "Dylan Strome", "F"),
    (120, "Zach Hyman", "F"),
    (121, "Shea Theodore", "D"),
    (122, "Roman Kantserov", "F"),
    (123, "JJ Peterka", "F"),
    (124, "Owen Tippett", "F"),
    (125, "Alexis Lafreniere", "F"),
    (126, "Morgan Geekie", "F"),
    (127, "Pavel Mintyukov", "D"),
    (128, "Mika Zibanejad", "F"),
    (129, "John Carlson", "D"),
    (130, "John Tavares", "F"),
    (131, "Tij Iginla", "F"),
    (132, "Mark Stone", "F"),
    (133, "Vincent Trocheck", "F"),
    (134, "Victor Hedman", "D"),
    (135, "Frank Nazar", "F"),
    (136, "Shayne Gostisbehere", "D"),
    (137, "J.T. Miller", "F"),
    (138, "Matty Beniers", "F"),
    (139, "Benjamin Kindel", "F"),
    (140, "Josh Doan", "F"),
    (141, "Denton Mateychuk", "D"),
    (142, "Simon Nemec", "D"),
    (143, "Artyom Levshunov", "D"),
    (144, "Mason McTavish", "F"),
    (145, "Tomas Hertl", "F"),
    (146, "Jackson Blake", "F"),
    (147, "Philip Broberg", "D"),
    (148, "Viggo Bjorck", "F"),
    (149, "Marco Rossi", "F"),
    (150, "Filip Hronek", "D"),
    (151, "Alex Laferriere", "F"),
    (152, "Tom Wilson", "F"),
    (153, "Anton Lundell", "F"),
    (154, "Nikolaj Ehlers", "F"),
    (155, "Alex Ovechkin", "F"),
    (156, "Sam Bennett", "F"),
    (157, "Keaton Verhoeff", "D"),
    (158, "Vince Dunn", "D"),
    (159, "Travis Sanheim", "D"),
    (160, "Aliaksei Protas", "F"),
    (161, "Jared McCann", "F"),
    (162, "Konsta Helenius", "F"),
    (163, "Matt Savoie", "F"),
    (164, "Carter Yakemchuk", "D"),
    (165, "Caleb Desnoyers", "F"),
    (166, "Brandon Montour", "D"),
    (167, "Darnell Nurse", "D"),
    (168, "Gabe Perreault", "F"),
    (169, "Aaron Ekblad", "D"),
    (170, "Kevin Fiala", "F"),
    (171, "MacKenzie Weegar", "D"),
    (172, "Dougie Hamilton", "D"),
    (173, "K'Andre Miller", "D"),
    (174, "Olen Zellweger", "D"),
    (175, "Michael Hage", "F"),
    (176, "Victor Eklund", "F"),
    (177, "Fraser Minten", "F"),
    (178, "Tyson Foerster", "F"),
    (179, "Timo Meier", "F"),
    (180, "Caleb Malhotra", "F"),
    (181, "Rasmus Andersson", "D"),
    (182, "Noah Hanifin", "D"),
    (183, "Alexander Zharovsky", "F"),
    (184, "Calum Ritchie", "F"),
    (185, "Brock Nelson", "F"),
    (186, "Brad Marchand", "F"),
    (187, "Ryan O'Reilly", "F"),
    (188, "Neal Pionk", "D"),
    (189, "Yegor Chinakhov", "F"),
    (190, "Igor Chernyshov", "F"),
    (191, "Devon Toews", "D"),
    (192, "Ilya Protas", "F"),
    (193, "Jacob Trouba", "D"),
    (194, "Sam Dickinson", "D"),
    (195, "Axel Sandin Pellikka", "D"),
    (196, "Jake O'Brien", "F"),
    (197, "Dalibor Dvorsky", "F"),
    (198, "Drew Doughty", "D"),
    (199, "Ivan Provorov", "D"),
    (200, "Martin Fehervary", "D"),
    (201, "Nazem Kadri", "F"),
    (202, "Ryan McDonagh", "D"),
    (203, "Jonas Brodin", "D"),
    (204, "Josh Norris", "F"),
    (205, "Steven Stamkos", "F"),
    (206, "Jamie Drysdale", "D"),
    (207, "Rasmus Sandin", "D"),
    (208, "Brent Burns", "D"),
    (209, "Evgeni Malkin", "F"),
    (210, "Bryan Rust", "F"),
    (211, "Mike Matheson", "D"),
    (212, "Luke Evangelista", "F"),
    (213, "Matt Coronato", "F"),
    (214, "Sean Walker", "D"),
    (215, "Ryan Nugent-Hopkins", "F"),
    (216, "Pavel Zacha", "F"),
    (217, "Mikael Granlund", "F"),
    (218, "Sam Rinzel", "D"),
    (219, "Bobby McMann", "F"),
    (220, "J.J. Moser", "D"),
    (221, "Valeri Nichushkin", "F"),
    (222, "Gustav Forsling", "D"),
    (223, "Justin Faulk", "D"),
    (224, "Sam Malinski", "D"),
    (225, "Jake DeBrusk", "F"),
    (226, "Morgan Rielly", "D"),
    (227, "Mattias Samuelsson", "D"),
    (228, "Oliver Ekman-Larsson", "D"),
    (229, "Sean Durzi", "D"),
    (230, "Luca Cagnoni", "D"),
    (231, "Kashawn Aitcheson", "D"),
    (232, "Tyler Bertuzzi", "F"),
    (233, "Nils Lundkvist", "D"),
    (234, "David Reinbacher", "D"),
    (235, "Patrick Kane", "F"),
    (236, "Jake Neighbours", "F"),
    (237, "Alberts Smits", "D"),
    (238, "Jalen Chatfield", "D"),
    (239, "Shane Pinto", "F"),
    (240, "Mason Marchment", "F"),
    (241, "Ivan Barbashev", "F"),
    (242, "Anthony DeAngelo", "D"),
    (243, "Jack Quinn", "F"),
    (244, "Jordan Spence", "D"),
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
for rank, name, pos in SKATER_DATA:
    key = normalize(name)
    if key in lookup:
        lookup[key][SOURCE_COL] = rank
    else:
        new_row = {fn: "" for fn in fieldnames}
        new_row["Player"] = name
        new_row["Position"] = pos
        new_row["Age"] = ""
        new_row[SOURCE_COL] = rank
        new_row["Average Rank"] = ""
        new_row["Rank Variance"] = ""
        new_players.append(new_row)
        rows.append(new_row)
        lookup[key] = new_row

with open(MASTER_PATH, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Merged {len(SKATER_DATA)} Dynasty Puck skaters.")
print(f"  Matched: {len(SKATER_DATA) - len(new_players)}")
print(f"  New players added: {len(new_players)}")
if new_players:
    for p in new_players:
        print(f"    + {p['Player']}")

subprocess.run(["python3", os.path.join(os.path.dirname(__file__), "recalculate.py"), MASTER_PATH])
