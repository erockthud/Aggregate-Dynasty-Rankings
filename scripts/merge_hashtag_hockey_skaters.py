#!/usr/bin/env python3
"""
Merge Hashtag Hockey (Mar 2026) skater rankings into hockey_skaters_master.csv.
Run recalculate.py afterward.
"""

import csv
import os
import re
import subprocess
import unicodedata

MASTER_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "hockey", "hockey_skaters_master.csv"))
SOURCE_COL = "Hashtag Hockey (Mar 2026)"

# (rank, name, position)  — position used only for new players not in master
HASHTAG_DATA = [
    (1, "Connor McDavid", "C"),
    (2, "Nathan MacKinnon", "C"),
    (3, "Leon Draisaitl", "LW"),
    (4, "Auston Matthews", "C"),
    (5, "Cale Makar", "D"),
    (6, "Jack Hughes", "C"),
    (7, "Nikita Kucherov", "RW"),
    (8, "David Pastrnak", "RW"),
    (9, "Connor Bedard", "C"),
    (10, "Kirill Kaprizov", "LW"),
    (11, "Matthew Tkachuk", "LW"),
    (12, "Quinn Hughes", "D"),
    (13, "Mitch Marner", "RW"),
    (14, "Jason Robertson", "LW"),
    (15, "Brady Tkachuk", "LW"),
    (16, "Mikko Rantanen", "RW"),
    (17, "Tim Stutzle", "C"),
    (18, "Macklin Celebrini", "C"),
    (19, "William Nylander", "RW"),
    (20, "Rasmus Dahlin", "D"),
    (21, "Jack Eichel", "C"),
    (22, "Brayden Point", "C"),
    (23, "Kyle Connor", "LW"),
    (24, "Artemi Panarin", "LW"),
    (25, "Jake Guentzel", "LW"),
    (26, "Aleksander Barkov", "C"),
    (27, "Sebastian Aho", "C"),
    (28, "Sam Reinhart", "RW"),
    (29, "Filip Forsberg", "LW"),
    (30, "Evan Bouchard", "D"),
    (31, "Matvei Michkov", "RW"),
    (32, "Adam Fox", "D"),
    (33, "J.T. Miller", "C"),
    (34, "Tage Thompson", "C"),
    (35, "Jesper Bratt", "RW"),
    (36, "Clayton Keller", "C"),
    (37, "Martin Necas", "C"),
    (38, "Brandon Hagel", "LW"),
    (39, "Elias Pettersson", "C"),
    (40, "Matt Boldy", "LW"),
    (41, "Lucas Raymond", "LW"),
    (42, "Dylan Larkin", "C"),
    (43, "Adrian Kempe", "C"),
    (44, "Travis Konecny", "RW"),
    (45, "Roman Josi", "D"),
    (46, "Roope Hintz", "C"),
    (47, "Andrei Svechnikov", "LW"),
    (48, "Mark Scheifele", "C"),
    (49, "Zach Werenski", "D"),
    (50, "Josh Morrissey", "D"),
    (51, "Jordan Kyrou", "C"),
    (52, "Alex DeBrincat", "LW"),
    (53, "Drake Batherson", "C"),
    (54, "Victor Hedman", "D"),
    (55, "Kevin Fiala", "C"),
    (56, "Nico Hischier", "C"),
    (57, "Nick Suzuki", "C"),
    (58, "Cole Caufield", "RW"),
    (59, "Seth Jarvis", "C"),
    (60, "Gabriel Vilardi", "C"),
    (61, "Shea Theodore", "D"),
    (62, "Logan Cooley", "C"),
    (63, "Marco Rossi", "C"),
    (64, "Nikolaj Ehlers", "LW"),
    (65, "Mathew Barzal", "C"),
    (66, "Ryan Nugent-Hopkins", "C"),
    (67, "Moritz Seider", "D"),
    (68, "Mika Zibanejad", "C"),
    (69, "Dylan Strome", "C"),
    (70, "Lane Hutson", "D"),
    (71, "Adam Fantilli", "C"),
    (72, "Steven Stamkos", "C"),
    (73, "Noah Dobson", "D"),
    (74, "Chris Kreider", "LW"),
    (75, "Sidney Crosby", "C"),
    (76, "Zach Hyman", "LW"),
    (77, "Robert Thomas", "C"),
    (78, "Miro Heiskanen", "D"),
    (79, "Dylan Guenther", "RW"),
    (80, "William Eklund", "LW"),
    (81, "John Tavares", "C"),
    (82, "Charlie McAvoy", "D"),
    (83, "Brock Boeser", "RW"),
    (84, "Alex Tuch", "RW"),
    (85, "Timo Meier", "RW"),
    (86, "Carter Verhaeghe", "C"),
    (87, "Dougie Hamilton", "D"),
    (88, "Valeri Nichushkin", "RW"),
    (89, "Leo Carlsson", "C"),
    (90, "Will Smith", "C"),
    (91, "Mason McTavish", "C"),
    (92, "Pavel Buchnevich", "RW"),
    (93, "Luke Hughes", "D"),
    (94, "Troy Terry", "C"),
    (95, "Tomas Hertl", "C"),
    (96, "Brock Nelson", "C"),
    (97, "Jake Sanderson", "D"),
    (98, "JJ Peterka", "RW"),
    (99, "Jonathan Huberdeau", "LW"),
    (100, "Brad Marchand", "LW"),
    (101, "Matt Duchene", "C"),
    (102, "Mark Stone", "RW"),
    (103, "Joel Eriksson Ek", "C"),
    (104, "Juraj Slafkovsky", "LW"),
    (105, "Nazem Kadri", "C"),
    (106, "Alex Ovechkin", "LW"),
    (107, "Bo Horvat", "C"),
    (108, "Vincent Trocheck", "C"),
    (109, "Erik Karlsson", "D"),
    (110, "MacKenzie Weegar", "D"),
    (111, "Jonathan Marchessault", "LW"),
    (112, "Nick Schmaltz", "C"),
    (113, "Tom Wilson", "RW"),
    (114, "Brock Faber", "D"),
    (115, "Owen Tippett", "RW"),
    (116, "Mikhail Sergachev", "D"),
    (117, "Tyler Toffoli", "RW"),
    (118, "John Carlson", "D"),
    (119, "Cole Perfetti", "C"),
    (120, "Patrik Laine", "RW"),
    (121, "Rickard Rakell", "C"),
    (122, "Matthew Knies", "LW"),
    (123, "Jared McCann", "LW"),
    (125, "Pierre-Luc Dubois", "C"),
    (126, "Mikael Granlund", "LW"),
    (127, "Trevor Zegras", "C"),
    (128, "Dylan Cozens", "C"),
    (129, "Morgan Rielly", "D"),
    (130, "Brandon Montour", "D"),
    (131, "Josh Norris", "C"),
    (132, "Aaron Ekblad", "D"),
    (133, "Logan Stankoven", "C"),
    (134, "Cutter Gauthier", "LW"),
    (135, "Vince Dunn", "D"),
    (136, "Jakob Chychrun", "D"),
    (137, "Matty Beniers", "C"),
    (138, "Alexis Lafreniere", "LW"),
    (139, "Shayne Gostisbehere", "D"),
    (140, "Artturi Lehkonen", "LW"),
    (141, "Thomas Chabot", "D"),
    (142, "Tyler Seguin", "C"),
    (143, "Brandt Clarke", "D"),
    (144, "Bryan Rust", "RW"),
    (145, "Anze Kopitar", "C"),
    (146, "Claude Giroux", "LW"),
    (147, "Evgeni Malkin", "C"),
    (148, "Mats Zuccarello", "RW"),
    (149, "Drew Doughty", "D"),
    (150, "Sam Bennett", "LW"),
    (151, "Teuvo Teravainen", "RW"),
    (152, "Kaapo Kakko", "RW"),
    (153, "Conor Garland", "RW"),
    (154, "Anders Lee", "LW"),
    (155, "Thomas Harley", "D"),
    (156, "Olen Zellweger", "D"),
    (157, "Mike Matheson", "D"),
    (158, "Elias Lindholm", "RW"),
    (159, "Gabriel Landeskog", "LW"),
    (160, "Evander Kane", "LW"),
    (161, "Michael Bunting", "LW"),
    (162, "Trevor Moore", "LW"),
    (163, "Yegor Sharangovich", "C"),
    (164, "Brayden Schenn", "C"),
    (165, "Kris Letang", "D"),
    (166, "Owen Power", "D"),
    (167, "Shane Wright", "C"),
    (168, "Simon Edvinsson", "D"),
    (169, "Seth Jones", "D"),
    (170, "Patrick Kane", "RW"),
    (171, "Gustav Forsling", "D"),
    (172, "Oliver Bjorkstrand", "RW"),
    (173, "Vladimir Tarasenko", "RW"),
    (174, "Devon Toews", "D"),
    (175, "Eeli Tolvanen", "LW"),
    (176, "Ryan O'Reilly", "C"),
    (177, "William Karlsson", "C"),
    (178, "Alex Pietrangelo", "D"),
    (179, "Simon Nemec", "D"),
    (180, "Jack Quinn", "RW"),
    (181, "Tommy Novak", "C"),
    (182, "Jeff Skinner", "LW"),
    (183, "Travis Sanheim", "D"),
    (184, "Viktor Arvidsson", "RW"),
    (185, "Mason Marchment", "LW"),
    (186, "Filip Hronek", "D"),
    (187, "Bowen Byram", "D"),
    (188, "Darnell Nurse", "D"),
    (189, "Andre Burakovsky", "LW"),
    (190, "David Perron", "RW"),
    (191, "Chandler Stephenson", "C"),
    (192, "Dawson Mercer", "C"),
    (193, "Taylor Hall", "LW"),
    (194, "Jamie Drysdale", "D"),
    (195, "Justin Faulk", "D"),
    (196, "Boone Jenner", "C"),
    (197, "David Jiricek", "D"),
    (198, "Adam Boqvist", "D"),
    (199, "Jacob Trouba", "D"),
    (200, "Brent Burns", "D"),
]


def normalize(name):
    name = unicodedata.normalize("NFKD", name)
    name = name.encode("ascii", "ignore").decode("ascii")
    name = name.lower()
    name = re.sub(r"\b(jr|sr|ii|iii|iv|v)\b\.?", "", name)
    name = re.sub(r"[^a-z\s]", "", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name


# Read master
with open(MASTER_PATH, newline="") as f:
    reader = csv.DictReader(f)
    fieldnames = list(reader.fieldnames)
    rows = list(reader)

# Add source column if not present
if SOURCE_COL not in fieldnames:
    fieldnames.insert(fieldnames.index("Average Rank"), SOURCE_COL)
    for row in rows:
        row[SOURCE_COL] = ""

# Build lookup
lookup = {normalize(row["Player"]): row for row in rows}

new_players = []
for rank, name, pos in HASHTAG_DATA:
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

print(f"Merged {len(HASHTAG_DATA)} Hashtag Hockey skaters.")
print(f"  Matched: {len(HASHTAG_DATA) - len(new_players)}")
print(f"  New players added: {len(new_players)}")
if new_players:
    for p in new_players:
        print(f"    + {p['Player']}")

subprocess.run(["python3", os.path.join(os.path.dirname(__file__), "recalculate.py"), MASTER_PATH])
