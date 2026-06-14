#!/usr/bin/env python3
"""
Update Dobber hockey skater rankings from Mar 2026 to Jun 2026.
Renames the column and replaces all values.
Run recalculate.py afterward.
"""

import csv
import os
import re
import subprocess
import unicodedata

MASTER_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "hockey", "hockey_skaters_master.csv"))
OLD_COL = "Dobber (Mar 2026)"
NEW_COL = "Dobber (Jun 2026)"

DOBBER_DATA = [
    (1, "Connor McDavid"),
    (2, "Nathan MacKinnon"),
    (3, "Nikita Kucherov"),
    (4, "Leon Draisaitl"),
    (5, "Macklin Celebrini"),
    (6, "Connor Bedard"),
    (7, "Martin Necas"),
    (8, "David Pastrnak"),
    (9, "Mitch Marner"),
    (10, "Jack Hughes"),
    (11, "Mikko Rantanen"),
    (12, "Jason Robertson"),
    (13, "Kirill Kaprizov"),
    (14, "Nick Suzuki"),
    (15, "Cale Makar"),
    (16, "Auston Matthews"),
    (17, "Jack Eichel"),
    (18, "William Nylander"),
    (19, "Quinn Hughes"),
    (20, "Evan Bouchard"),
    (21, "Cole Caufield"),
    (22, "Tim Stutzle"),
    (23, "Kyle Connor"),
    (24, "Mark Scheifele"),
    (25, "Tage Thompson"),
    (26, "Matthew Tkachuk"),
    (27, "Matt Boldy"),
    (28, "Sam Reinhart"),
    (29, "Sebastian Aho"),
    (30, "Jesper Bratt"),
    (31, "Jake Guentzel"),
    (32, "Wyatt Johnston"),
    (33, "Clayton Keller"),
    (34, "Artemi Panarin"),
    (35, "Lane Hutson"),
    (36, "Brandon Hagel"),
    (37, "Brady Tkachuk"),
    (38, "Rasmus Dahlin"),
    (39, "Robert Thomas"),
    (40, "Lucas Raymond"),
    (41, "Zach Werenski"),
    (42, "Leo Carlsson"),
    (43, "Ivan Demidov"),
    (44, "Alex DeBrincat"),
    (45, "Aleksander Barkov"),
    (46, "Adam Fantilli"),
    (47, "Travis Konecny"),
    (48, "Brayden Point"),
    (49, "Juraj Slafkovsky"),
    (50, "Logan Cooley"),
    (51, "Cutter Gauthier"),
    (52, "Elias Pettersson"),
    (53, "Marco Rossi"),
    (54, "Dylan Guenther"),
    (55, "Nico Hischier"),
    (56, "Kirill Marchenko"),
    (57, "Drake Batherson"),
    (58, "Mathew Barzal"),
    (59, "Matvei Michkov"),
    (60, "Filip Forsberg"),
    (61, "Dylan Larkin"),
    (62, "Trevor Zegras"),
    (63, "Andrei Svechnikov"),
    (64, "Roope Hintz"),
    (65, "Matthew Knies"),
    (66, "Will Smith"),
    (67, "Dylan Holloway"),
    (68, "Adrian Kempe"),
    (69, "Sidney Crosby"),
    (70, "Nikolaj Ehlers"),
    (71, "Seth Jarvis"),
    (72, "Mark Stone"),
    (73, "Troy Terry"),
    (74, "Josh Morrissey"),
    (75, "Matthew Schaefer"),
    (76, "Adam Fox"),
    (77, "Mika Zibanejad"),
    (78, "Morgan Geekie"),
    (79, "Miro Heiskanen"),
    (80, "J.T. Miller"),
    (81, "Mikhail Sergachev"),
    (82, "Anton Frondell"),
    (83, "Tomas Hertl"),
    (84, "Pavel Dorofeyev"),
    (85, "Alex Tuch"),
    (86, "Anton Lundell"),
    (87, "Quinton Byfield"),
    (88, "Dylan Strome"),
    (89, "Alexis Lafreniere"),
    (90, "Ryan Nugent-Hopkins"),
    (91, "Dylan Cozens"),
    (92, "Matty Beniers"),
    (93, "Jake Sanderson"),
    (94, "Logan Stankoven"),
    (95, "Gabriel Vilardi"),
    (96, "Moritz Seider"),
    (97, "Pierre-Luc Dubois"),
    (98, "Noah Dobson"),
    (99, "William Eklund"),
    (100, "Beckett Sennecke"),
    (101, "Darren Raddysh"),
    (102, "Porter Martone"),
    (103, "Bo Horvat"),
    (104, "Ryan Leonard"),
    (105, "Nick Schmaltz"),
    (106, "Shea Theodore"),
    (107, "Jakob Chychrun"),
    (108, "Connor McMichael"),
    (109, "John Tavares"),
    (110, "Jared McCann"),
    (111, "Tom Wilson"),
    (112, "Michael Misa"),
    (113, "Frank Nazar"),
    (114, "Charlie McAvoy"),
    (115, "JJ Peterka"),
    (116, "Kevin Fiala"),
    (117, "Jack Quinn"),
    (118, "Matt Duchene"),
    (119, "Jordan Kyrou"),
    (120, "Erik Karlsson"),
    (121, "Pavel Zacha"),
    (122, "Brock Nelson"),
    (123, "Joel Eriksson Ek"),
    (124, "Aliaksei Protas"),
    (125, "Ivan Barbashev"),
    (126, "Bryan Rust"),
    (127, "Zach Hyman"),
    (128, "Carter Verhaeghe"),
    (129, "Owen Tippett"),
    (130, "Brad Marchand"),
    (131, "Cole Hutson"),
    (132, "Timo Meier"),
    (133, "Luke Evangelista"),
    (134, "Jackson Blake"),
    (135, "Zach Benson"),
    (136, "Thomas Harley"),
    (137, "Josh Doan"),
    (138, "Patrick Kane"),
    (139, "Victor Hedman"),
    (140, "Kaapo Kakko"),
    (141, "Jackson Lacombe"),
    (142, "Valeri Nichushkin"),
    (143, "Ryan McLeod"),
    (144, "Alex Ovechkin"),
    (145, "Vince Dunn"),
    (146, "Mavrik Bourque"),
    (147, "Brock Boeser"),
    (148, "Vincent Trocheck"),
    (149, "Ryan O'Reilly"),
    (150, "Steven Stamkos"),
    (151, "John Carlson"),
    (152, "Luke Hughes"),
    (153, "Nazem Kadri"),
    (154, "Yegor Chinakhov"),
    (155, "Mason McTavish"),
    (156, "Anthony Cirelli"),
    (157, "Shayne Gostisbehere"),
    (158, "Sam Bennett"),
    (159, "Elias Lindholm"),
    (160, "James Hagens"),
    (161, "Cole Perfetti"),
    (162, "Sean Monahan"),
    (163, "Tyler Toffoli"),
    (164, "Brandt Clarke"),
    (165, "Konsta Helenius"),
    (166, "Matt Coronato"),
    (167, "Brock Faber"),
    (168, "Filip Hronek"),
    (169, "Shane Wright"),
    (170, "Pavel Buchnevich"),
    (171, "Artyom Levshunov"),
    (172, "Mackie Samoskevich"),
    (173, "Kent Johnson"),
    (174, "Shane Pinto"),
    (175, "Barrett Hayton"),
    (176, "Morgan Frost"),
    (177, "Bowen Byram"),
    (178, "Mason Marchment"),
    (179, "Roman Josi"),
    (180, "Jimmy Snuggerud"),
    (181, "Evgeni Malkin"),
    (182, "Anthony Mantha"),
    (183, "Matias Maccelli"),
    (184, "Bobby McMann"),
    (185, "Alex Laferriere"),
    (186, "Matt Savoie"),
    (187, "Rickard Rakell"),
    (188, "Simon Nemec"),
    (189, "Dawson Mercer"),
    (190, "Alex Newhook"),
    (191, "Bobby Brink"),
    (192, "Benjamin Kindel"),
    (193, "Peyton Krebs"),
    (194, "Tyson Foerster"),
    (195, "Jamie Drysdale"),
    (196, "Teuvo Teravainen"),
    (197, "Fraser Minten"),
    (198, "Tyler Seguin"),
    (199, "Tyler Bertuzzi"),
    (200, "Claude Giroux"),
    (201, "Berkly Catton"),
    (202, "Artturi Lehkonen"),
    (203, "Collin Graf"),
    (204, "Axel Sandin Pellikka"),
    (205, "Igor Chernyshov"),
    (206, "Denton Mateychuk"),
    (207, "Rasmus Andersson"),
    (208, "Jake Neighbours"),
    (209, "Will Cuylle"),
    (210, "Jiri Kulich"),
    (211, "Ryan Donato"),
    (212, "Zayne Parekh"),
    (213, "Viktor Arvidsson"),
    (214, "Justin Sourdif"),
    (215, "Alexander Nikishin"),
    (216, "Jonathan Huberdeau"),
    (217, "Noah Ostlund"),
    (218, "Josh Norris"),
    (219, "Cole Sillinger"),
    (220, "Tij Iginla"),
    (221, "Gabe Perreault"),
    (222, "Easton Cowan"),
    (223, "Alexander Wennberg"),
    (224, "Jake DeBrusk"),
    (225, "Matvei Gridin"),
    (226, "Chandler Stephenson"),
    (227, "Zeev Buium"),
    (228, "Zack Bolduc"),
    (229, "Connor Zary"),
    (230, "William Karlsson"),
    (231, "Noah Hanifin"),
    (232, "Emil Heineman"),
    (233, "Owen Power"),
    (234, "Nicholas Robertson"),
    (235, "Danila Yurov"),
    (236, "Taylor Hall"),
    (237, "Casey Mittelstadt"),
    (238, "Roman Kantserov"),
    (239, "Chris Kreider"),
    (240, "Eeli Tolvanen"),
    (241, "Jordan Eberle"),
    (242, "Sean Durzi"),
    (243, "Mats Zuccarello"),
    (244, "Seth Jones"),
    (245, "Charlie Coyle"),
    (246, "Alex Bump"),
    (247, "Conor Garland"),
    (248, "Mikael Granlund"),
    (249, "Dmitri Voronkov"),
    (250, "Brett Howden"),
    (251, "Calum Ritchie"),
    (252, "Thomas Chabot"),
    (253, "Gage Goncalves"),
    (254, "Dougie Hamilton"),
    (255, "Patrik Laine"),
    (256, "Vasily Podkolzin"),
    (257, "Arseniy Gritsyuk"),
    (258, "Kirby Dach"),
    (259, "Nick Lardis"),
    (260, "Simon Holmstrom"),
    (261, "Brady Martin"),
    (262, "K'Andre Miller"),
    (263, "Jamie Benn"),
    (264, "Dalibor Dvorsky"),
    (265, "Anders Lee"),
    (266, "Sam Dickinson"),
    (267, "Lawson Crouse"),
    (268, "Jason Zucker"),
    (269, "Noah Cates"),
    (270, "Denver Barkey"),
    (271, "Jack Roslovic"),
    (272, "Mike Matheson"),
    (273, "Andrew Cristall"),
    (274, "Jordan Spence"),
    (275, "Jonathan Lekkerimaki"),
    (276, "Ridly Greig"),
    (277, "Tommy Novak"),
    (278, "Caleb Desnoyers"),
    (279, "Matthew Wood"),
    (280, "Cole Eiserman"),
    (281, "Rutger McGroarty"),
    (282, "Ilya Protas"),
    (283, "Andre Burakovsky"),
    (284, "Nick Paul"),
    (285, "Gabriel Landeskog"),
    (286, "Cayden Lindstrom"),
    (287, "Brandon Montour"),
    (288, "Emmitt Finnie"),
    (289, "Liam Greentree"),
    (290, "Bradly Nadeau"),
    (291, "Michael Bunting"),
    (292, "Oliver Moore"),
    (293, "Oliver Kapanen"),
    (294, "Morgan Rielly"),
    (295, "Joel Farabee"),
    (296, "Justin Brazeau"),
    (297, "Roger McQueen"),
    (298, "Kailer Yamamoto"),
    (299, "Aaron Ekblad"),
    (300, "Ivan Miroshnichenko"),
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
for rank, name in DOBBER_DATA:
    key = normalize(name)
    if key in lookup:
        lookup[key][NEW_COL] = rank
    else:
        unmatched.append((rank, name))
        new_row = {fn: "" for fn in fieldnames}
        new_row["Player"] = name
        new_row["Position"] = ""
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
