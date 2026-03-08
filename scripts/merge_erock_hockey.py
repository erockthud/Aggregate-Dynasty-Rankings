"""Add ErockThud (Mar 2026) rankings to hockey skaters and goalies masters.
Combined skaters+goalies list; split by matching against existing master files.
"""
import csv, io, re, subprocess, unicodedata

SKATERS_PATH = "hockey/hockey_skaters_master.csv"
GOALIES_PATH = "hockey/hockey_goalies_master.csv"
NEW_COL = "ErockThud (Mar 2026)"

def normalize(name):
    name = unicodedata.normalize("NFKD", name)
    name = name.encode("ascii", "ignore").decode("ascii")
    name = name.lower()
    name = re.sub(r"\b(jr|sr|ii|iii|iv|v)\b\.?", "", name)
    name = re.sub(r"[^a-z\s]", "", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name

# Source name → canonical master name
NAME_MAP = {
    "johnjason peterka": "jj peterka",
    "matthew beniers": "matty beniers",
    "zachary bolduc": "zack bolduc",
    "matthew coronato": "matt coronato",
    "arseny gritsyuk": "arseniy gritsyuk",
    "jon marchessault": "jonathan marchessault",
    "matthew samoskevich": "mackie samoskevich",
    "joshua norris": "josh norris",
    "zachary benson": "zach benson",
    "matthew boldy": "matt boldy",
    "gabriel perreault": "gabe perreault",
    "matthew savoie": "matt savoie",
    # Typos in this source
    "sam dickenson": "sam dickinson",
    "artyom levhunov": "artyom levshunov",
    "axel sandid pellikka": "axel sandin pellikka",
}

# Source data: (rank, name)  — draft pick entries will be filtered out
RANKINGS = [
    (1, "Connor McDavid"),
    (2, "Nathan MacKinnon"),
    (3, "Leon Draisaitl"),
    (4, "Macklin Celebrini"),
    (5, "Connor Bedard"),
    (6, "Cale Makar"),
    (7, "Nikita Kucherov"),
    (8, "Jack Hughes"),
    (9, "Quinn Hughes"),
    (10, "David Pastrnak"),
    (11, "Kirill Kaprizov"),
    (12, "Matthew Schaefer"),
    (13, "Rasmus Dahlin"),
    (14, "Tim Stutzle"),
    (15, "Wyatt Johnston"),
    (16, "Auston Matthews"),
    (17, "Mikko Rantanen"),
    (18, "Jake Oettinger"),
    (19, "Matthew Boldy"),
    (20, "William Nylander"),
    (21, "Jack Eichel"),
    (22, "Lane Hutson"),
    (23, "Ivan Demidov"),
    (24, "Evan Bouchard"),
    (25, "Connor Hellebuyck"),
    (26, "Jason Robertson"),
    (27, "Seth Jarvis"),
    (28, "Zach Werenski"),
    (29, "Mitch Marner"),
    (30, "Adam Fantilli"),
    (31, "Igor Shesterkin"),
    (32, "Lucas Raymond"),
    (33, "Adam Fox"),
    (34, "Brady Tkachuk"),
    (35, "Cole Caufield"),
    (36, "Logan Cooley"),
    (37, "Andrei Vasilevskiy"),
    (38, "Kyle Connor"),
    (39, "Tage Thompson"),
    (40, "Matthew Tkachuk"),
    (41, "Jake Sanderson"),
    (42, "Nick Suzuki"),
    (43, "Brandon Hagel"),
    (44, "Kirill Marchenko"),
    (45, "Filip Forsberg"),
    (46, "Clayton Keller"),
    (47, "Will Smith"),
    (48, "Brayden Point"),
    (49, "Jesper Bratt"),
    (50, "Dylan Guenther"),
    (51, "Miro Heiskanen"),
    (52, "Sam Reinhart"),
    (53, "Quinton Byfield"),
    (54, "Logan Thompson"),
    (55, "Jake Guentzel"),
    (56, "Michael Misa"),
    (57, "Artemi Panarin"),
    (58, "Moritz Seider"),
    (59, "Mark Scheifele"),
    (60, "Sebastian Aho"),
    (61, "Ilya Sorokin"),
    # 62 = draft pick, skip
    (63, "Matvei Michkov"),
    (64, "Filip Gustavsson"),
    (65, "Martin Necas"),
    (66, "Leo Carlsson"),
    (67, "Juraj Slafkovsky"),
    (68, "Dylan Holloway"),
    (69, "Spencer Knight"),
    (70, "Alex DeBrincat"),
    (71, "Nico Hischier"),
    (72, "Yaroslav Askarov"),
    (73, "Matthew Knies"),
    (74, "Adrian Kempe"),
    (75, "Jeremy Swayman"),
    (76, "Jackson LaCombe"),
    (77, "Pavel Dorofeyev"),
    (78, "Thomas Harley"),
    (79, "Dustin Wolf"),
    (80, "Dylan Larkin"),
    (81, "Luke Hughes"),
    (82, "Elias Pettersson"),
    (83, "J.T. Miller"),
    (84, "Juuse Saros"),
    (85, "Brandt Clarke"),
    (86, "Mason McTavish"),
    (87, "Jakob Chychrun"),
    (88, "Josh Morrissey"),
    (89, "John-Jason Peterka"),
    (90, "Trevor Zegras"),
    (91, "Robert Thomas"),
    (92, "Travis Konecny"),
    (93, "Mackenzie Blackwood"),
    (94, "Kevin Fiala"),
    (95, "Noah Dobson"),
    (96, "Andrei Svechnikov"),
    (97, "Jordan Kyrou"),
    (98, "Zayne Parekh"),
    (99, "Roope Hintz"),
    (100, "Gabriel Vilardi"),
    (101, "Charlie McAvoy"),
    (102, "Victor Hedman"),
    (103, "Alexander Nikishin"),
    (104, "Karel Vejmelka"),
    (105, "Marco Rossi"),
    (106, "Sam Rinzel"),
    (107, "Cutter Gauthier"),
    (108, "Frank Nazar"),
    (109, "Matthew Beniers"),
    (110, "William Eklund"),
    (111, "Nikolaj Ehlers"),
    (112, "Drake Batherson"),
    (113, "Matthew Coronato"),
    (114, "Darcy Kuemper"),
    (115, "Will Cuylle"),
    (116, "Lukas Dostal"),
    (117, "Sidney Crosby"),
    (118, "Cole Perfetti"),
    (119, "Carter Verhaeghe"),
    (120, "Shea Theodore"),
    (121, "Aliaksei Protas"),
    (122, "Logan Stankoven"),
    (123, "Ryan Leonard"),
    (124, "Mikhail Sergachev"),
    (125, "Timo Meier"),
    (126, "Marco Kasper"),
    (127, "Zach Hyman"),
    (128, "Mathew Barzal"),
    (129, "Dylan Cozens"),
    (130, "Dougie Hamilton"),
    (131, "Aleksander Barkov"),
    (132, "MacKenzie Weegar"),
    (133, "Roman Josi"),
    (134, "Darren Raddysh"),
    (135, "Thatcher Demko"),
    (136, "Joey Daccord"),
    (137, "Zachary Bolduc"),
    (138, "Alex Tuch"),
    (139, "Joel Eriksson Ek"),
    (140, "Anton Lundell"),
    (141, "Alex Laferriere"),
    (142, "Connor McMichael"),
    (143, "Simon Edvinsson"),
    (144, "Sergei Bobrovsky"),
    (145, "Kent Johnson"),
    (146, "Jimmy Snuggerud"),
    (147, "John Tavares"),
    (148, "Cole Hutson"),
    (149, "Vincent Trocheck"),
    (150, "Jordan Binnington"),
    (151, "Jacob Markstrom"),
    (152, "Linus Ullmark"),
    (153, "Sam Dickenson"),
    (154, "Jiri Kulich"),
    (155, "Shane Wright"),
    (156, "James Hagens"),
    (157, "Brock Faber"),
    (158, "Tyson Foerster"),
    (159, "Mika Zibanejad"),
    (160, "Adin Hill"),
    (161, "Jackson Blake"),
    (162, "Anton Frondell"),
    (163, "Owen Tippett"),
    (164, "Stuart Skinner"),
    (165, "Morgan Geekie"),
    (166, "Tyler Toffoli"),
    (167, "Dylan Strome"),
    (168, "Alexis Lafreniere"),
    # 169 = draft pick, skip
    (170, "Brock Boeser"),
    (171, "Bo Horvat"),
    (172, "Pierre-Luc Dubois"),
    (173, "Philip Broberg"),
    (174, "Sam Montembeault"),
    (175, "Tom Wilson"),
    (176, "Shane Pinto"),
    # 177 = draft pick, skip
    (178, "Owen Power"),
    (179, "Zeev Buium"),
    (180, "Erik Karlsson"),
    (181, "Steven Stamkos"),
    (182, "Anthony Stolarz"),
    (183, "Alexander Romanov"),
    (184, "Ryan Nugent-Hopkins"),
    (185, "Valeri Nichushkin"),
    (186, "Tomas Hertl"),
    # 187 = draft pick, skip
    (188, "Nazem Kadri"),
    (189, "Joseph Woll"),
    (190, "Olen Zellweger"),
    (191, "Dmitri Voronkov"),
    (192, "Ukko-Pekka Luukkonen"),
    (193, "Kaiden Guhle"),
    (194, "Pyotr Kochetkov"),
    (195, "Pavel Buchnevich"),
    (196, "Rickard Rakell"),
    (197, "Troy Terry"),
    (198, "Alex Ovechkin"),
    (199, "John Carlson"),
    (200, "K'Andre Miller"),
    (201, "Morgan Rielly"),
    (202, "Connor Zary"),
    (203, "Alex Vlasic"),
    (204, "Logan Mailloux"),
    (205, "Vince Dunn"),
    (206, "Zachary Benson"),
    # 207 = draft pick, skip
    (208, "Brock Nelson"),
    (209, "Mark Stone"),
    (210, "Bowen Byram"),
    (211, "Thomas Chabot"),
    (212, "Kaapo Kakko"),
    (213, "Chris Kreider"),
    (214, "Sam Bennett"),
    (215, "Artyom Levhunov"),
    (216, "Matt Duchene"),
    (217, "Jared McCann"),
    (218, "Nick Schmaltz"),
    (219, "Artturi Lehkonen"),
    (220, "Maxim Shabanov"),
    (221, "Aaron Ekblad"),
    (222, "Brad Marchand"),
    (223, "Seth Jones"),
    (224, "Noah Hanifin"),
    (225, "Devon Toews"),
    (226, "Bryan Rust"),
    (227, "Elias Lindholm"),
    (228, "John Gibson"),
    (229, "Conor Garland"),
    (230, "Filip Hronek"),
    (231, "Carter Yakemchuk"),
    (232, "Jonathan Huberdeau"),
    (233, "Gabe Perreault"),
    (234, "Michael Kesselring"),
    (235, "Mattias Ekholm"),
    (236, "Ryan O'Reilly"),
    (237, "Luke Evangelista"),
    (238, "Anthony Cirelli"),
    (239, "Ridly Greig"),
    (240, "Rasmus Andersson"),
    (241, "Dawson Mercer"),
    (242, "Barrett Hayton"),
    (243, "Cole Sillinger"),
    (244, "Gabriel Landeskog"),
    (245, "Samuel Ersson"),
    (246, "Jake Walman"),
    (247, "Jake Neighbours"),
    (248, "Patrik Laine"),
    (249, "Gustav Forsling"),
    (250, "Elvis Merzlikins"),
    (251, "Brandon Montour"),
    (252, "Neal Pionk"),
    (253, "Sean Durzi"),
    (254, "Sean Monahan"),
    (255, "Caleb Desnoyers"),
    (256, "Anze Kopitar"),
    (257, "Darnell Nurse"),
    (258, "Frederik Andersen"),
    (259, "Braden Schneider"),
    (260, "Mason Marchment"),
    (261, "Frank Vatrano"),
    (262, "Simon Holmstrom"),
    (263, "Mikael Granlund"),
    (264, "Anders Lee"),
    (265, "Joshua Norris"),
    (266, "Travis Sanheim"),
    (267, "Jack Quinn"),
    (268, "Beckett Sennecke"),
    (269, "Shayne Gostisbehere"),
    (270, "Jake Debrusk"),
    (271, "Dylan Samberg"),
    (272, "Drew Doughty"),
    (273, "Dante Fabbro"),
    (274, "Trevor Moore"),
    (275, "Mike Matheson"),
    (276, "Cameron York"),
    (277, "Filip Chytil"),
    (278, "Eeli Tolvanen"),
    (279, "Colton Parayko"),
    (280, "Mats Zuccarello"),
    (281, "William Karlsson"),
    (282, "Mason Lohrei"),
    (283, "Arseny Gritsyuk"),
    (284, "Boone Jenner"),
    (285, "Patrick Kane"),
    (286, "Evgeni Malkin"),
    (287, "Morgan Frost"),
    (288, "Anthony DeAngelo"),
    (289, "Kris Letang"),
    (290, "Jet Greaves"),
    (291, "Jaccob Slavin"),
    # 292 = draft pick, skip
    (293, "Yegor Sharangovich"),
    (294, "Jon Marchessault"),
    (295, "Ryan Donato"),
    (296, "Tij Iginla"),
    (297, "Jamie Drysdale"),
    (298, "Brayden Schenn"),
    (299, "Jordan Spence"),
    (300, "Pavel Zacha"),
    (301, "Justin Faulk"),
    (302, "Josh Doan"),
    (303, "Ivan Barbashev"),
    (304, "Oliver Bjorkstrand"),
    (305, "Rasmus Sandin"),
    (306, "Teuvo Teravainen"),
    (307, "Warren Foegele"),
    (308, "Evander Kane"),
    (309, "Blake Coleman"),
    (310, "Jacob Trouba"),
    (311, "Viktor Arvidsson"),
    (312, "Mikey Anderson"),
    (313, "Brady Skjei"),
    (314, "Esa Lindell"),
    (315, "Phillip Danault"),
    (316, "Jacob Middleton"),
    (317, "Bobby McMann"),
    (318, "Jake McCabe"),
    (319, "Ryan Pulock"),
    (320, "Brent Burns"),
    (321, "Fabian Zetterlund"),
    (322, "Jesperi Kotkaniemi"),
    (323, "Hampus Lindholm"),
    (324, "Jared Spurgeon"),
    (325, "Cam Fowler"),
    (326, "Vladislav Gavrikov"),
    (327, "Denton Mateychuk"),
    (328, "Ivan Provorov"),
    (329, "Adam Larsson"),
    (330, "Axel Sandid Pellikka"),
    (331, "Brayden McNabb"),
    (332, "Samuel Girard"),
    (333, "Matt Roy"),
    (334, "Ryan McLeod"),
    (335, "Jonas Brodin"),
    (336, "Marcus Pettersson"),
    (337, "Scott Morrow"),
    (338, "Ross Colton"),
    (339, "Casey Mittelstadt"),
    (340, "J.J. Moser"),
    (341, "Sean Couturier"),
    (342, "Matthew Samoskevich"),
    (343, "Mikael Backlund"),
    (344, "Sam Malinski"),
    (345, "Jamie Benn"),
    (346, "Yegor Chinakhov"),
    (347, "Nick Seeler"),
    (348, "Stefan Noesen"),
    (349, "Martin Fehervary"),
    (350, "Oliver Ekman-Larsson"),
    (351, "Ryan McDonagh"),
    (352, "Matias Maccelli"),
    (353, "Jason Zucker"),
    (354, "Tyler Seguin"),
    (355, "Dylan DeMelo"),
    (356, "Jaden Schwartz"),
    (357, "Radko Gudas"),
    (358, "Kyle Palmieri"),
    (359, "Timothy Liljegren"),
    (360, "Evan Rodrigues"),
    (361, "Chris Tanev"),
    (362, "Pius Suter"),
    (363, "Brett Pesce"),
    (364, "Cody Ceci"),
    (365, "Brett Kulak"),
    (366, "Alexandre Carrier"),
    (367, "Artem Zub"),
    (368, "Tyler Myers"),
    (369, "Brett Howden"),
    (370, "Nicolas Roy"),
    (371, "Nikita Zadorov"),
    (372, "Berkly Catton"),
    (373, "Porter Martone"),
]

def read_master(path):
    with open(path, newline='', encoding='utf-8') as f:
        rows = list(csv.reader(f))
    return rows

def build_lookup(rows):
    """normalized_name → row_index (1-based into rows list)"""
    lookup = {}
    for i, row in enumerate(rows[1:], 1):
        if row:
            lookup[normalize(row[0])] = i
    return lookup

def add_col(rows, col_name):
    """Insert new source column before Average Rank."""
    header = rows[0]
    avg_idx = header.index('Average Rank')
    for row in rows:
        if len(row) >= avg_idx:
            row.insert(avg_idx, '')
    rows[0][avg_idx] = col_name
    return avg_idx

def write_master(path, rows):
    out = io.StringIO()
    csv.writer(out).writerows(rows)
    with open(path, 'w', newline='', encoding='utf-8') as f:
        f.write(out.getvalue())

# Load masters
sk_rows = read_master(SKATERS_PATH)
go_rows = read_master(GOALIES_PATH)

sk_lookup = build_lookup(sk_rows)
go_lookup = build_lookup(go_rows)

# Add new column to both masters
sk_col_idx = add_col(sk_rows, NEW_COL)
go_col_idx = add_col(go_rows, NEW_COL)

sk_matched = sk_new = go_matched = go_new = 0
unmatched = []

for rank, name in RANKINGS:
    key = normalize(name)
    key = NAME_MAP.get(key, key)

    if key in sk_lookup:
        sk_rows[sk_lookup[key]][sk_col_idx] = rank
        sk_matched += 1
    elif key in go_lookup:
        go_rows[go_lookup[key]][go_col_idx] = rank
        go_matched += 1
    else:
        # New player — need to determine which file
        # Goalies known by name pattern — none new here; default to skaters
        # Add as new skater row
        new_row = [''] * len(sk_rows[0])
        new_row[0] = name
        new_row[1] = 'F'   # default; will fix manually if wrong
        new_row[sk_col_idx] = rank
        sk_rows.append(new_row)
        sk_lookup[key] = len(sk_rows) - 1
        sk_new += 1
        unmatched.append((rank, name))

write_master(SKATERS_PATH, sk_rows)
write_master(GOALIES_PATH, go_rows)

print(f"Skaters: {sk_matched} matched, {sk_new} new")
print(f"Goalies: {go_matched} matched")
if unmatched:
    print("\nNew players added to skaters (verify position):")
    for rank, name in unmatched:
        print(f"  {rank}. {name}")

# Recalculate both
for path in [SKATERS_PATH, GOALIES_PATH]:
    subprocess.run(["python3", "scripts/recalculate.py", path], check=True)
    print(f"Recalculated {path}")
