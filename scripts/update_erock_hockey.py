"""Update ErockThud (Mar 2026) -> ErockThud (Sep 2026) hockey rankings.
Combined skaters+goalies list; split by matching against existing master files,
then re-ranked sequentially 1-N within each group by order of appearance
(draft pick slots already filtered out of RANKINGS below).
"""
import csv, io, re, subprocess, unicodedata

SKATERS_PATH = "hockey/hockey_skaters_master.csv"
GOALIES_PATH = "hockey/hockey_goalies_master.csv"
OLD_COL = "ErockThud (Mar 2026)"
NEW_COL = "ErockThud (Sep 2026)"

def normalize(name):
    name = unicodedata.normalize("NFKD", name)
    name = name.encode("ascii", "ignore").decode("ascii")
    name = name.lower()
    name = re.sub(r"\b(jr|sr|ii|iii|iv|v)\b\.?", "", name)
    name = re.sub(r"[^a-z\s]", "", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name

# Source name -> canonical master name
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
    "sam dickenson": "sam dickinson",
    "artyom levhunov": "artyom levshunov",
    "axel sandid pellikka": "axel sandin pellikka",
}

# (rank, name) — draft pick entries already filtered out
RANKINGS = [
    (1, 'Macklin Celebrini'),
    (2, 'Connor McDavid'),
    (3, 'Nathan MacKinnon'),
    (4, 'Cale Makar'),
    (5, 'Connor Bedard'),
    (6, 'Leon Draisaitl'),
    (7, 'Matthew Schaefer'),
    (8, 'Jack Hughes'),
    (9, 'Quinn Hughes'),
    (10, 'David Pastrnak'),
    (11, 'Kirill Kaprizov'),
    (12, 'Nikita Kucherov'),
    (13, 'Matthew Boldy'),
    (14, 'Auston Matthews'),
    (15, 'Jason Robertson'),
    (16, 'Rasmus Dahlin'),
    (17, 'Lane Hutson'),
    (18, 'Mikko Rantanen'),
    (19, 'Wyatt Johnston'),
    (20, 'Jack Eichel'),
    (21, 'Evan Bouchard'),
    (22, 'Tim Stutzle'),
    (23, 'Zach Werenski'),
    (24, 'Martin Necas'),
    (25, 'Igor Shesterkin'),
    (26, 'Mitch Marner'),
    (27, 'Gavin McKenna'),
    (28, 'Cole Caufield'),
    (29, 'Ivan Demidov'),
    (30, 'Leo Carlsson'),
    (31, 'Adam Fox'),
    (32, 'Kyle Connor'),
    (33, 'Jake Oettinger'),
    (34, 'Adam Fantilli'),
    (35, 'Andrei Vasilevskiy'),
    (36, 'William Nylander'),
    (37, 'Will Smith'),
    (38, 'Lucas Raymond'),
    (39, 'Brady Tkachuk'),
    (40, 'Logan Cooley'),
    (41, 'Connor Hellebuyck'),
    (42, 'Nick Suzuki'),
    (43, 'Dylan Guenther'),
    (44, 'Seth Jarvis'),
    (45, 'Matthew Tkachuk'),
    (46, 'Cutter Gauthier'),
    (47, 'Jake Sanderson'),
    (48, 'Kirill Marchenko'),
    (49, 'Michael Misa'),
    (50, 'Ivar Stenberg'),
    (51, 'Tage Thompson'),
    (52, 'Logan Thompson'),
    (53, 'Beckett Sennecke'),
    (54, 'Ilya Sorokin'),
    (55, 'Moritz Seider'),
    (56, 'Miro Heiskanen'),
    (57, 'Sam Reinhart'),
    (58, 'Matvei Michkov'),
    (59, 'Yaroslav Askarov'),
    (60, 'Porter Martone'),
    (61, 'Jeremy Swayman'),
    (62, 'Clayton Keller'),
    (63, 'Jake Guentzel'),
    (64, 'Darren Raddysh'),
    (65, 'Brandon Hagel'),
    (66, 'Sebastian Aho'),
    (67, 'Juraj Slafkovsky'),
    (68, 'Filip Forsberg'),
    (69, 'Alex DeBrincat'),
    (70, 'Jesper Bratt'),
    (71, 'Brayden Point'),
    (72, 'Brandt Clarke'),
    (73, 'Mark Scheifele'),
    (74, 'Spencer Knight'),
    (75, 'Dustin Wolf'),
    (76, 'Jakob Chychrun'),
    (77, 'Adrian Kempe'),
    (78, 'Cole Hutson'),
    (79, 'Filip Gustavsson'),
    (81, 'Matthew Knies'),
    (82, 'Dylan Larkin'),
    (83, 'Thomas Harley'),
    (84, 'Robert Thomas'),
    (85, 'Dylan Holloway'),
    (86, 'Jimmy Snuggerud'),
    (87, 'Jackson LaCombe'),
    (88, 'Artemi Panarin'),
    (89, 'Nico Hischier'),
    (90, 'Charlie McAvoy'),
    (91, 'Pavel Dorofeyev'),
    (92, 'Mikhail Sergachev'),
    (93, 'Karel Vejmelka'),
    (94, 'Travis Konecny'),
    (95, 'Jordan Kyrou'),
    (96, 'Quinton Byfield'),
    (97, 'Juuse Saros'),
    (98, 'Andrei Svechnikov'),
    (99, 'Aleksander Barkov'),
    (100, 'Josh Morrissey'),
    (101, 'Trevor Zegras'),
    (102, 'John-Jason Peterka'),
    (103, 'Zayne Parekh'),
    (104, 'Anton Frondell'),
    (105, 'Mason McTavish'),
    (106, 'Lukas Dostal'),
    (107, 'Alexander Nikishin'),
    (108, 'Gabe Perreault'),
    (109, 'Luke Hughes'),
    (110, 'Ryan Leonard'),
    (111, 'Frank Nazar'),
    (112, 'Elias Pettersson'),
    (113, 'Alexis Lafreniere'),
    (114, 'James Hagens'),
    (115, 'William Eklund'),
    (116, 'Logan Stankoven'),
    (117, 'Matthew Beniers'),
    (118, 'J.T. Miller'),
    (119, 'Kevin Fiala'),
    (120, 'Nikolaj Ehlers'),
    (121, 'Noah Dobson'),
    (122, 'Drake Batherson'),
    (123, 'Shea Theodore'),
    (124, 'Timo Meier'),
    (125, 'Zach Hyman'),
    (126, 'Anton Lundell'),
    (127, 'Bo Horvat'),
    (128, 'Roman Kantserov'),
    (129, 'Matthew Coronato'),
    (130, 'Mathew Barzal'),
    (131, 'Dylan Cozens'),
    (132, 'Marco Rossi'),
    (133, 'Cole Perfetti'),
    (134, 'Roope Hintz'),
    (135, 'Sidney Crosby'),
    (136, 'Roman Josi'),
    (138, 'Joel Eriksson Ek'),
    (139, 'Alex Tuch'),
    (140, 'Morgan Geekie'),
    (141, 'Owen Tippett'),
    (142, 'Simon Edvinsson'),
    (143, 'Zeev Buium'),
    (144, 'Brock Boeser'),
    (145, 'Will Cuylle'),
    (146, 'Carter Verhaeghe'),
    (147, 'Sergei Bobrovsky'),
    (148, 'Dougie Hamilton'),
    (149, 'Linus Ullmark'),
    (150, 'Nick Schmaltz'),
    (151, 'Scott Wedgewood'),
    (152, 'Mika Zibanejad'),
    (153, 'Luke Evangelista'),
    (154, 'Mackenzie Blackwood'),
    (155, 'Brock Faber'),
    (156, 'Jordan Binnington'),
    (157, 'John Carlson'),
    (158, 'Tij Iginla'),
    (159, 'Joey Daccord'),
    (160, 'Jacob Markstrom'),
    (161, 'Zachary Bolduc'),
    (162, 'John Tavares'),
    (163, 'Sam Dickenson'),
    (164, 'Gabriel Vilardi'),
    (165, 'Ilya Protas'),
    (166, 'Aliaksei Protas'),
    (167, 'Alex Laferriere'),
    (168, 'Marco Kasper'),
    (169, 'Jackson Blake'),
    (170, 'Erik Karlsson'),
    (171, 'Mark Stone'),
    (172, 'Shane Wright'),
    (173, 'Jack Quinn'),
    (174, 'Dylan Strome'),
    (175, 'Philip Broberg'),
    (176, 'Tom Wilson'),
    (177, 'Caleb Desnoyers'),
    (178, 'Owen Power'),
    (179, 'Shayne Gostisbehere'),
    (180, 'Darcy Kuemper'),
    (181, 'Steven Stamkos'),
    (182, 'Pierre-Luc Dubois'),
    (183, 'Connor McMichael'),
    (184, 'Valeri Nichushkin'),
    (185, 'Pyotr Kochetkov'),
    (186, 'Carter Yakemchuk'),
    (187, 'Shane Pinto'),
    (188, 'Tomas Hertl'),
    (189, 'Vincent Trocheck'),
    (190, 'Tyler Toffoli'),
    (192, 'Olen Zellweger'),
    (193, 'MacKenzie Weegar'),
    (194, 'Thatcher Demko'),
    (195, 'Dmitri Voronkov'),
    (196, 'Kent Johnson'),
    (197, 'Ukko-Pekka Luukkonen'),
    (198, 'Kaiden Guhle'),
    (199, 'Pavel Buchnevich'),
    (200, 'Rickard Rakell'),
    (201, 'Seth Jones'),
    (202, 'Ryan Nugent-Hopkins'),
    (203, 'Troy Terry'),
    (204, 'Alex Ovechkin'),
    (205, "K'Andre Miller"),
    (206, 'Morgan Rielly'),
    (207, 'Alex Vlasic'),
    (208, 'Logan Mailloux'),
    (209, 'Vince Dunn'),
    (210, 'Pavel Zacha'),
    (211, 'Tyson Foerster'),
    (212, 'Zachary Benson'),
    (214, 'Jiri Kulich'),
    (215, 'Brock Nelson'),
    (216, 'Bowen Byram'),
    (217, 'Nazem Kadri'),
    (218, 'Thomas Chabot'),
    (219, 'Kaapo Kakko'),
    (220, 'Stuart Skinner'),
    (221, 'Sam Bennett'),
    (222, 'Artyom Levhunov'),
    (223, 'Matt Duchene'),
    (224, 'Jamie Drysdale'),
    (225, 'Victor Hedman'),
    (226, 'Jared McCann'),
    (227, 'Artturi Lehkonen'),
    (228, 'Maxim Shabanov'),
    (229, 'Adin Hill'),
    (230, 'Sam Montembeault'),
    (231, 'Brad Marchand'),
    (232, 'Noah Hanifin'),
    (233, 'Connor Zary'),
    (234, 'Devon Toews'),
    (235, 'Bryan Rust'),
    (236, 'Elias Lindholm'),
    (237, 'John Gibson'),
    (238, 'Sam Rinzel'),
    (239, 'Conor Garland'),
    (240, 'Gabriel Landeskog'),
    (241, 'Anthony Stolarz'),
    (242, 'Berkly Catton'),
    (243, "Ryan O'Reilly"),
    (244, 'Filip Hronek'),
    (245, 'Jonathan Huberdeau'),
    (246, 'Michael Kesselring'),
    (247, 'Mattias Ekholm'),
    (248, 'Anthony Cirelli'),
    (249, 'Ridly Greig'),
    (250, 'Rasmus Andersson'),
    (251, 'Dawson Mercer'),
    (252, 'Barrett Hayton'),
    (253, 'Jake Walman'),
    (254, 'Alexander Romanov'),
    (255, 'Jake Neighbours'),
    (256, 'Patrik Laine'),
    (257, 'Gustav Forsling'),
    (258, 'Elvis Merzlikins'),
    (259, 'Brandon Montour'),
    (260, 'Neal Pionk'),
    (261, 'Sean Durzi'),
    (262, 'Sean Monahan'),
    (263, 'Darnell Nurse'),
    (264, 'Chris Kreider'),
    (265, 'Frederik Andersen'),
    (266, 'Braden Schneider'),
    (267, 'Joseph Woll'),
    (268, 'Mason Marchment'),
    (269, 'Frank Vatrano'),
    (270, 'Simon Holmstrom'),
    (271, 'Mikael Granlund'),
    (272, 'Anders Lee'),
    (273, 'Joshua Norris'),
    (274, 'Travis Sanheim'),
    (275, 'Jake Debrusk'),
    (276, 'Dylan Samberg'),
    (277, 'Drew Doughty'),
    (278, 'Cole Sillinger'),
    (279, 'Dante Fabbro'),
    (280, 'Trevor Moore'),
    (281, 'Mike Matheson'),
    (282, 'Cameron York'),
    (283, 'Filip Chytil'),
    (284, 'Eeli Tolvanen'),
    (285, 'Colton Parayko'),
    (286, 'Mats Zuccarello'),
    (287, 'William Karlsson'),
    (288, 'Mason Lohrei'),
    (289, 'Arseny Gritsyuk'),
    (290, 'Boone Jenner'),
    (291, 'Patrick Kane'),
    (292, 'Evgeni Malkin'),
    (293, 'Morgan Frost'),
    (294, 'Anthony DeAngelo'),
    (295, 'Kris Letang'),
    (296, 'Jet Greaves'),
    (297, 'Jaccob Slavin'),
    (299, 'Yegor Sharangovich'),
    (300, 'Jon Marchessault'),
    (301, 'Ryan Donato'),
    (302, 'Brayden Schenn'),
    (303, 'Jordan Spence'),
    (304, 'Justin Faulk'),
    (305, 'Josh Doan'),
    (306, 'Aaron Ekblad'),
    (307, 'Ivan Barbashev'),
    (308, 'Oliver Bjorkstrand'),
    (309, 'Rasmus Sandin'),
    (310, 'Teuvo Teravainen'),
    (311, 'Warren Foegele'),
    (312, 'Evander Kane'),
    (313, 'Blake Coleman'),
    (314, 'Jacob Trouba'),
    (315, 'Viktor Arvidsson'),
    (316, 'Mikey Anderson'),
    (317, 'Brady Skjei'),
    (318, 'Esa Lindell'),
    (319, 'Phillip Danault'),
    (320, 'Jacob Middleton'),
    (321, 'Bobby McMann'),
    (322, 'Jake McCabe'),
    (323, 'Ryan Pulock'),
    (324, 'Brent Burns'),
    (325, 'Fabian Zetterlund'),
    (326, 'Jesperi Kotkaniemi'),
    (327, 'Hampus Lindholm'),
    (328, 'Jared Spurgeon'),
    (329, 'Cam Fowler'),
    (330, 'Vladislav Gavrikov'),
    (331, 'Denton Mateychuk'),
    (332, 'Ivan Provorov'),
    (333, 'Adam Larsson'),
    (334, 'Axel Sandid Pellikka'),
    (335, 'Brayden McNabb'),
    (336, 'Samuel Girard'),
    (337, 'Matt Roy'),
    (338, 'Ryan McLeod'),
    (339, 'Jonas Brodin'),
    (340, 'Samuel Ersson'),
    (341, 'Marcus Pettersson'),
    (342, 'Scott Morrow'),
    (343, 'Ross Colton'),
    (344, 'Casey Mittelstadt'),
    (345, 'J.J. Moser'),
    (346, 'Sean Couturier'),
    (347, 'Matthew Samoskevich'),
    (348, 'Mikael Backlund'),
    (349, 'Sam Malinski'),
    (350, 'Jamie Benn'),
    (351, 'Yegor Chinakhov'),
    (352, 'Nick Seeler'),
    (353, 'Stefan Noesen'),
    (354, 'Martin Fehervary'),
    (355, 'Oliver Ekman-Larsson'),
    (356, 'Ryan McDonagh'),
    (357, 'Matias Maccelli'),
    (358, 'Jason Zucker'),
    (359, 'Tyler Seguin'),
    (360, 'Dylan DeMelo'),
    (361, 'Jaden Schwartz'),
    (362, 'Radko Gudas'),
    (363, 'Kyle Palmieri'),
    (364, 'Timothy Liljegren'),
    (365, 'Evan Rodrigues'),
    (366, 'Chris Tanev'),
    (367, 'Pius Suter'),
    (368, 'Brett Pesce'),
    (369, 'Cody Ceci'),
    (370, 'Brett Kulak'),
    (371, 'Alexandre Carrier'),
    (372, 'Artem Zub'),
    (373, 'Tyler Myers'),
    (374, 'Brett Howden'),
    (375, 'Nicolas Roy'),
    (376, 'Nikita Zadorov'),
]

def read_master(path):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.reader(f))

def build_lookup(rows):
    lookup = {}
    for i, row in enumerate(rows[1:], 1):
        if row:
            lookup[normalize(row[0])] = i
    return lookup

def write_master(path, rows):
    out = io.StringIO()
    csv.writer(out).writerows(rows)
    with open(path, 'w', newline='', encoding='utf-8') as f:
        f.write(out.getvalue())

sk_rows = read_master(SKATERS_PATH)
go_rows = read_master(GOALIES_PATH)

sk_lookup = build_lookup(sk_rows)
go_lookup = build_lookup(go_rows)

sk_col_idx = sk_rows[0].index(OLD_COL)
go_col_idx = go_rows[0].index(OLD_COL)

sk_rows[0][sk_col_idx] = NEW_COL
go_rows[0][go_col_idx] = NEW_COL

for row in sk_rows[1:]:
    if len(row) > sk_col_idx:
        row[sk_col_idx] = ''
for row in go_rows[1:]:
    if len(row) > go_col_idx:
        row[go_col_idx] = ''

sk_entries = []
go_entries = []
unmatched = []

for orig_rank, name in RANKINGS:
    key = normalize(name)
    key = NAME_MAP.get(key, key)
    if key in sk_lookup:
        sk_entries.append((orig_rank, name, sk_lookup[key]))
    elif key in go_lookup:
        go_entries.append((orig_rank, name, go_lookup[key]))
    else:
        unmatched.append((orig_rank, name))

for seq_rank, (orig_rank, name, row_idx) in enumerate(sk_entries, 1):
    sk_rows[row_idx][sk_col_idx] = seq_rank

for seq_rank, (orig_rank, name, row_idx) in enumerate(go_entries, 1):
    go_rows[row_idx][go_col_idx] = seq_rank

write_master(SKATERS_PATH, sk_rows)
write_master(GOALIES_PATH, go_rows)

print(f"Skaters matched/re-ranked: {len(sk_entries)}")
print(f"Goalies matched/re-ranked: {len(go_entries)}")
print(f"Unmatched: {len(unmatched)}")
for orig_rank, name in unmatched:
    print(f"  {orig_rank}\t{name}")

for path in [SKATERS_PATH, GOALIES_PATH]:
    subprocess.run(["python3", "scripts/recalculate.py", path], check=True)
    print(f"Recalculated {path}")
