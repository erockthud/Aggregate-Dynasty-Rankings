#!/usr/bin/env python3
"""
Update Dobber hockey skater rankings from Jun 2026 to Aug 2026.
Renames the column and replaces all values.
Run recalculate.py afterward.
"""

import csv
import os
import re
import subprocess
import unicodedata

MASTER_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "hockey", "hockey_skaters_master.csv"))
OLD_COL = "Dobber (Jun 2026)"
NEW_COL = "Dobber (Aug 2026)"

DOBBER_DATA = [
    (1, "Connor McDavid", "F"),
    (2, "Nathan MacKinnon", "F"),
    (3, "Nikita Kucherov", "F"),
    (4, "Leon Draisaitl", "F"),
    (5, "Macklin Celebrini", "F"),
    (6, "Martin Necas", "F"),
    (7, "David Pastrnak", "F"),
    (8, "Jason Robertson", "F"),
    (9, "Mitch Marner", "F"),
    (10, "Jack Hughes", "F"),
    (11, "Connor Bedard", "F"),
    (12, "Nick Suzuki", "F"),
    (13, "Kirill Kaprizov", "F"),
    (14, "Jack Eichel", "F"),
    (15, "Cale Makar", "D"),
    (16, "Mikko Rantanen", "F"),
    (17, "William Nylander", "F"),
    (18, "Kyle Connor", "F"),
    (19, "Cole Caufield", "F"),
    (20, "Quinn Hughes", "D"),
    (21, "Tim Stutzle", "F"),
    (22, "Evan Bouchard", "D"),
    (23, "Clayton Keller", "F"),
    (24, "Matt Boldy", "F"),
    (25, "Mark Scheifele", "F"),
    (26, "Artemi Panarin", "F"),
    (27, "Wyatt Johnston", "F"),
    (28, "Auston Matthews", "F"),
    (29, "Jesper Bratt", "F"),
    (30, "Jake Guentzel", "F"),
    (31, "Sebastian Aho", "F"),
    (32, "Matthew Tkachuk", "F"),
    (33, "Tage Thompson", "F"),
    (34, "Alex DeBrincat", "F"),
    (35, "Lane Hutson", "D"),
    (36, "Brandon Hagel", "F"),
    (37, "Ivan Demidov", "F"),
    (38, "Sam Reinhart", "F"),
    (39, "Juraj Slafkovsky", "F"),
    (40, "Rasmus Dahlin", "D"),
    (41, "Zach Werenski", "D"),
    (42, "Leo Carlsson", "F"),
    (43, "Robert Thomas", "F"),
    (44, "Adam Fantilli", "F"),
    (45, "Lucas Raymond", "F"),
    (46, "Brayden Point", "F"),
    (47, "Dylan Guenther", "F"),
    (48, "Aleksander Barkov", "F"),
    (49, "Brady Tkachuk", "F"),
    (50, "Cutter Gauthier", "F"),
    (51, "Matvei Michkov", "F"),
    (52, "Filip Forsberg", "F"),
    (53, "Drake Batherson", "F"),
    (54, "Kirill Marchenko", "F"),
    (55, "Travis Konecny", "F"),
    (56, "Logan Cooley", "F"),
    (57, "Sidney Crosby", "F"),
    (58, "Elias Pettersson", "F"),
    (59, "Dylan Larkin", "F"),
    (60, "Nikolaj Ehlers", "F"),
    (61, "Beckett Sennecke", "F"),
    (62, "Gavin McKenna", "F"),
    (63, "Adrian Kempe", "F"),
    (64, "Adam Fox", "D"),
    (65, "Nico Hischier", "F"),
    (66, "Andrei Svechnikov", "F"),
    (67, "Will Smith", "F"),
    (68, "Mathew Barzal", "F"),
    (69, "Alexis Lafreniere", "F"),
    (70, "Dylan Strome", "F"),
    (71, "Matthew Knies", "F"),
    (72, "Dylan Holloway", "F"),
    (73, "Anton Frondell", "F"),
    (74, "Marco Rossi", "F"),
    (75, "J.T. Miller", "F"),
    (76, "Trevor Zegras", "F"),
    (77, "Ivar Stenberg", "F"),
    (78, "Matthew Schaefer", "D"),
    (79, "Quinton Byfield", "F"),
    (80, "Mika Zibanejad", "F"),
    (81, "Morgan Geekie", "F"),
    (82, "Josh Morrissey", "D"),
    (83, "Nick Schmaltz", "F"),
    (84, "Mikhail Sergachev", "D"),
    (85, "Gabriel Vilardi", "F"),
    (86, "Roope Hintz", "F"),
    (87, "Mark Stone", "F"),
    (88, "Miro Heiskanen", "D"),
    (89, "Jake Sanderson", "D"),
    (90, "Michael Misa", "F"),
    (91, "Shea Theodore", "D"),
    (92, "Porter Martone", "F"),
    (93, "Jordan Kyrou", "F"),
    (94, "Matty Beniers", "F"),
    (95, "Ryan Leonard", "F"),
    (96, "Pavel Dorofeyev", "F"),
    (97, "JJ Peterka", "F"),
    (98, "Dylan Cozens", "F"),
    (99, "Logan Stankoven", "F"),
    (100, "Connor McMichael", "F"),
    (101, "Bo Horvat", "F"),
    (102, "Moritz Seider", "D"),
    (103, "John Tavares", "F"),
    (104, "William Eklund", "F"),
    (105, "John Carlson", "D"),
    (106, "Noah Dobson", "D"),
    (107, "Aliaksei Protas", "F"),
    (108, "Jack Quinn", "F"),
    (109, "Ryan Nugent-Hopkins", "F"),
    (110, "Josh Doan", "F"),
    (111, "Pavel Zacha", "F"),
    (112, "Kevin Fiala", "F"),
    (113, "Darren Raddysh", "D"),
    (114, "Anton Lundell", "F"),
    (115, "Jared McCann", "F"),
    (116, "Jakob Chychrun", "D"),
    (117, "Zach Benson", "F"),
    (118, "Seth Jarvis", "F"),
    (119, "Pierre-Luc Dubois", "F"),
    (120, "Tom Wilson", "F"),
    (121, "Charlie McAvoy", "D"),
    (122, "Matt Duchene", "F"),
    (123, "Jackson Lacombe", "D"),
    (124, "Zach Hyman", "F"),
    (125, "Ryan O'Reilly", "F"),
    (126, "Bryan Rust", "F"),
    (127, "Bowen Byram", "D"),
    (128, "Roman Kantserov", "F"),
    (129, "Luke Evangelista", "F"),
    (130, "Cole Hutson", "D"),
    (131, "Carter Verhaeghe", "F"),
    (132, "Alex Tuch", "F"),
    (133, "Tomas Hertl", "F"),
    (134, "Ivan Barbashev", "F"),
    (135, "Jackson Blake", "F"),
    (136, "Erik Karlsson", "D"),
    (137, "Vincent Trocheck", "F"),
    (138, "Brad Marchand", "F"),
    (139, "Matt Coronato", "F"),
    (140, "Matvei Gridin", "F"),
    (141, "Brock Boeser", "F"),
    (142, "Kaapo Kakko", "F"),
    (143, "Mason McTavish", "F"),
    (144, "Brock Nelson", "F"),
    (145, "Nazem Kadri", "F"),
    (146, "Igor Chernyshov", "F"),
    (147, "Steven Stamkos", "F"),
    (148, "Timo Meier", "F"),
    (149, "Konsta Helenius", "F"),
    (150, "Jimmy Snuggerud", "F"),
    (151, "Troy Terry", "F"),
    (152, "Gabe Perreault", "F"),
    (153, "Luke Hughes", "D"),
    (154, "Shayne Gostisbehere", "D"),
    (155, "Owen Tippett", "F"),
    (156, "Frank Nazar", "F"),
    (157, "Thomas Harley", "D"),
    (158, "Simon Nemec", "D"),
    (159, "Matt Savoie", "F"),
    (160, "Sam Bennett", "F"),
    (161, "Brandt Clarke", "D"),
    (162, "Valeri Nichushkin", "F"),
    (163, "Anthony Cirelli", "F"),
    (164, "Mavrik Bourque", "F"),
    (165, "Vince Dunn", "D"),
    (166, "Tyson Foerster", "F"),
    (167, "Yegor Chinakhov", "F"),
    (168, "Zack Bolduc", "F"),
    (169, "Cole Perfetti", "F"),
    (170, "Rickard Rakell", "F"),
    (171, "Victor Eklund", "F"),
    (172, "Zayne Parekh", "D"),
    (173, "Joel Eriksson Ek", "F"),
    (174, "Kent Johnson", "F"),
    (175, "Patrick Kane", "F"),
    (176, "Filip Hronek", "D"),
    (177, "Tyler Toffoli", "F"),
    (178, "Ryan McLeod", "F"),
    (179, "Roman Josi", "D"),
    (180, "Pavel Buchnevich", "F"),
    (181, "Ben Kindel", "F"),
    (182, "Shane Pinto", "F"),
    (183, "Shane Wright", "F"),
    (184, "Anthony Mantha", "F"),
    (185, "Brock Faber", "D"),
    (186, "Alex Ovechkin", "F"),
    (187, "Alex Newhook", "F"),
    (188, "Morgan Frost", "F"),
    (189, "Victor Hedman", "D"),
    (190, "Artyom Levshunov", "D"),
    (191, "Viggo Bjorck", "F"),
    (192, "Peyton Krebs", "F"),
    (193, "Jonathan Huberdeau", "F"),
    (194, "James Hagens", "F"),
    (195, "Dawson Mercer", "F"),
    (196, "Mason Marchment", "F"),
    (197, "Alex Laferriere", "F"),
    (198, "Mackie Samoskevich", "F"),
    (199, "Tij Iginla", "F"),
    (200, "Josh Norris", "F"),
    (201, "Berkly Catton", "F"),
    (202, "Teuvo Teravainen", "F"),
    (203, "Jake Neighbours", "F"),
    (204, "Evgeni Malkin", "F"),
    (205, "Tyler Bertuzzi", "F"),
    (206, "Mikael Granlund", "F"),
    (207, "Jamie Drysdale", "D"),
    (208, "Maxim Shabanov", "F"),
    (209, "Brett Howden", "F"),
    (210, "Matias Maccelli", "F"),
    (211, "Arseniy Gritsyuk", "F"),
    (212, "Connor Zary", "F"),
    (213, "Axel Sandin Pellikka", "D"),
    (214, "Vasily Podkolzin", "F"),
    (215, "Owen Power", "D"),
    (216, "Bobby McMann", "F"),
    (217, "Alexander Nikishin", "D"),
    (218, "Bobby Brink", "F"),
    (219, "Claude Giroux", "F"),
    (220, "Chandler Stephenson", "F"),
    (221, "Easton Cowan", "F"),
    (222, "Will Cuylle", "F"),
    (223, "Fraser Minten", "F"),
    (224, "Denton Mateychuk", "D"),
    (225, "Emil Heineman", "F"),
    (226, "Sean Monahan", "F"),
    (227, "Nicholas Robertson", "F"),
    (228, "Chase Reid", "D"),
    (229, "Artturi Lehkonen", "F"),
    (230, "Barrett Hayton", "F"),
    (231, "Zeev Buium", "D"),
    (232, "Justin Sourdif", "F"),
    (233, "Mats Zuccarello", "F"),
    (234, "Rasmus Andersson", "D"),
    (235, "Elias Lindholm", "F"),
    (236, "Calum Ritchie", "F"),
    (237, "Cole Sillinger", "F"),
    (238, "Jake DeBrusk", "F"),
    (239, "Alexander Wennberg", "F"),
    (240, "Emmitt Finnie", "F"),
    (241, "Jordan Eberle", "F"),
    (242, "Carter Yakemchuk", "D"),
    (243, "William Karlsson", "F"),
    (244, "Dmitri Voronkov", "F"),
    (245, "Eeli Tolvanen", "F"),
    (246, "Casey Mittelstadt", "F"),
    (247, "Charlie Stramel", "F"),
    (248, "Denver Barkey", "F"),
    (249, "Andrew Cristall", "F"),
    (250, "Noah Ostlund", "F"),
    (251, "Gage Goncalves", "F"),
    (252, "Brady Martin", "F"),
    (253, "Oliver Moore", "F"),
    (254, "Collin Graf", "F"),
    (255, "Dalibor Dvorsky", "F"),
    (256, "Viktor Arvidsson", "F"),
    (257, "Roger McQueen", "F"),
    (258, "Simon Holmstrom", "F"),
    (259, "Sam Dickinson", "D"),
    (260, "Tyler Seguin", "F"),
    (261, "Noah Hanifin", "D"),
    (262, "Danila Yurov", "F"),
    (263, "Jiri Kulich", "F"),
    (264, "Charlie Coyle", "F"),
    (265, "Ridly Greig", "F"),
    (266, "Caleb Desnoyers", "F"),
    (267, "Nick Lardis", "F"),
    (268, "Liam Ruck", "F"),
    (269, "Conor Garland", "F"),
    (270, "Taylor Hall", "F"),
    (271, "Matthew Wood", "F"),
    (272, "Caleb Malhotra", "F"),
    (273, "Jake O'Brien", "F"),
    (274, "Kirby Dach", "F"),
    (275, "Justin Hryckowian", "F"),
    (276, "Jackson Smith", "D"),
    (277, "Jason Zucker", "F"),
    (278, "Ilya Protas", "F"),
    (279, "Jack Roslovic", "F"),
    (280, "Liam Greentree", "F"),
    (281, "Chris Kreider", "F"),
    (282, "K'Andre Miller", "D"),
    (283, "Alex Bump", "F"),
    (284, "Ryan Greene", "F"),
    (285, "Vitali Pinchuk", "F"),
    (286, "Joel Farabee", "F"),
    (287, "Noah Cates", "F"),
    (288, "Rutger McGroarty", "F"),
    (289, "Cole Eiserman", "F"),
    (290, "Jordan Spence", "D"),
    (291, "Jagger Firkus", "F"),
    (292, "Lawson Crouse", "F"),
    (293, "Alexander Zharovsky", "F"),
    (294, "Wyatt Cullen", "F"),
    (295, "Ivan Miroshnichenko", "F"),
    (296, "Dougie Hamilton", "D"),
    (297, "Jonathan Lekkerimaki", "F"),
    (298, "Patrik Laine", "F"),
    (299, "Trevor Connelly", "F"),
    (300, "Kyle Palmieri", "F"),
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

# Rename column header
if OLD_COL in fieldnames:
    fieldnames[fieldnames.index(OLD_COL)] = NEW_COL
    for row in rows:
        row[NEW_COL] = row.pop(OLD_COL, "")

# Clear existing Dobber values
for row in rows:
    row[NEW_COL] = ""

# Build lookup
lookup = {normalize(row["Player"]): row for row in rows}

new_players = []
unmatched = []
for rank, name, pos in DOBBER_DATA:
    key = normalize(name)
    if key in lookup:
        lookup[key][NEW_COL] = rank
    else:
        unmatched.append((rank, name))
        new_row = {fn: "" for fn in fieldnames}
        new_row["Player"] = name
        new_row["Position"] = pos
        new_row["Age"] = ""
        new_row[NEW_COL] = rank
        new_row["Average Rank"] = ""
        new_row["Rank Variance"] = ""
        new_players.append(new_row)
        rows.append(new_row)
        lookup[key] = new_row

with open(MASTER_PATH, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Updated {len(DOBBER_DATA)} Dobber skater rankings ({OLD_COL} -> {NEW_COL}).")
print(f"  Matched: {len(DOBBER_DATA) - len(new_players)}")
print(f"  New players added: {len(new_players)}")
if new_players:
    for rank, name in unmatched:
        print(f"    + [{rank}] {name}")

subprocess.run(["python3", os.path.join(os.path.dirname(__file__), "recalculate.py"), MASTER_PATH])
