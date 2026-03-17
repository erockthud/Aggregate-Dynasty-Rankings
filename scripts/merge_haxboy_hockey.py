"""Add Haxboy (Mar 2026) rankings to hockey skaters and goalies masters.
Combined skaters+goalies list; split by matching against existing master files.
Draft pick entries are filtered out. Each group is re-ranked sequentially 1-N.
"""
import csv, io, re, subprocess, unicodedata

SKATERS_PATH = "hockey/hockey_skaters_master.csv"
GOALIES_PATH = "hockey/hockey_goalies_master.csv"
NEW_COL = "Haxboy (Mar 2026)"

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
    "matthew boldy":      "matt boldy",
    "johnjason peterka":  "jj peterka",
    "matthew beniers":    "matty beniers",
    "zachary bolduc":     "zack bolduc",
    "matthew coronato":   "matt coronato",
    "joshua norris":      "josh norris",
    "gabriel perreault":  "gabe perreault",
    "sam dickenson":      "sam dickinson",
}

# Source data from CSV (draft pick rows already excluded below)
RANKINGS_RAW = [
    (1,   "Connor McDavid"),
    (2,   "Macklin Celebrini"),
    (3,   "Nathan MacKinnon"),
    (4,   "Connor Bedard"),
    (5,   "Cale Makar"),
    (6,   "Leon Draisaitl"),
    (7,   "Jack Hughes"),
    (8,   "Quinn Hughes"),
    (9,   "Kirill Kaprizov"),
    (10,  "Tim Stutzle"),
    (11,  "Matthew Boldy"),
    (12,  "Wyatt Johnston"),
    (13,  "Leo Carlsson"),
    (14,  "David Pastrnak"),
    (15,  "Mikko Rantanen"),
    (16,  "Auston Matthews"),
    (17,  "Jason Robertson"),
    (18,  "Brady Tkachuk"),
    (19,  "Mitch Marner"),
    (20,  "Jack Eichel"),
    (21,  "Evan Bouchard"),
    (22,  "Nikita Kucherov"),
    (23,  "Rasmus Dahlin"),
    (24,  "Jake Oettinger"),
    (25,  "Connor Hellebuyck"),
    (26,  "Igor Shesterkin"),
    (27,  "Andrei Vasilevskiy"),
    (28,  "Ilya Sorokin"),
    (29,  "Lane Hutson"),
    (30,  "Matthew Tkachuk"),
    (31,  "Cole Caufield"),
    (32,  "Lucas Raymond"),
    (33,  "Seth Jarvis"),
    (34,  "Zach Werenski"),
    (35,  "Tage Thompson"),
    (36,  "Martin Necas"),
    (37,  "Brandon Hagel"),
    (38,  "Clayton Keller"),
    (39,  "Adam Fox"),
    (40,  "Adam Fantilli"),
    (41,  "Dylan Guenther"),
    (42,  "Will Smith"),
    (43,  "Cutter Gauthier"),
    (44,  "Ivan Demidov"),
    (45,  "Logan Cooley"),
    (46,  "Matthew Schaefer"),
    (47,  "Michael Misa"),
    (48,  "Kirill Marchenko"),
    (49,  "Kyle Connor"),
    (50,  "William Nylander"),
    (51,  "Brayden Point"),
    (52,  "Jake Sanderson"),
    (53,  "Matvei Michkov"),
    (54,  "Adrian Kempe"),
    (55,  "Jeremy Swayman"),
    (56,  "Dustin Wolf"),
    (57,  "Moritz Seider"),
    (58,  "Miro Heiskanen"),
    (59,  "Juraj Slafkovsky"),
    (60,  "Nick Suzuki"),
    (61,  "Sam Reinhart"),
    (62,  "Jake Guentzel"),
    (63,  "Sebastian Aho"),
    (64,  "Alex DeBrincat"),
    (65,  "Pavel Dorofeyev"),
    (66,  "Beckett Sennecke"),
    (67,  "Jesper Bratt"),
    (68,  "Dylan Holloway"),
    (69,  "Drake Batherson"),
    (70,  "Jakob Chychrun"),
    (71,  "Robert Thomas"),
    # 72 = draft pick, skip
    (73,  "Travis Konecny"),
    (74,  "Gabriel Vilardi"),
    (75,  "Jackson LaCombe"),
    (76,  "Spencer Knight"),
    (77,  "Lukas Dostal"),
    (78,  "Alex Tuch"),
    (79,  "Mathew Barzal"),
    (80,  "Nico Hischier"),
    (81,  "Andrei Svechnikov"),
    (82,  "Noah Dobson"),
    (83,  "Matthew Knies"),
    (84,  "Mikhail Sergachev"),
    (85,  "Thomas Harley"),
    (86,  "Logan Thompson"),
    (87,  "Quinton Byfield"),
    (88,  "Aleksander Barkov"),
    (89,  "Luke Hughes"),
    (90,  "Elias Pettersson"),
    (91,  "Jordan Kyrou"),
    (92,  "John-Jason Peterka"),
    (93,  "Mark Scheifele"),
    (94,  "Josh Morrissey"),
    (95,  "Dylan Larkin"),
    (96,  "Bo Horvat"),
    (97,  "Filip Forsberg"),
    (98,  "Artemi Panarin"),
    (99,  "Trevor Zegras"),
    (100, "Kevin Fiala"),
    (101, "Nikolaj Ehlers"),
    (102, "Filip Gustavsson"),
    (103, "Charlie McAvoy"),
    (104, "Brandt Clarke"),
    (105, "Mackenzie Blackwood"),
    (106, "Karel Vejmelka"),
    (107, "Roope Hintz"),
    (108, "Juuse Saros"),
    (109, "Mika Zibanejad"),
    (110, "Tij Iginla"),
    (111, "William Eklund"),
    (112, "Zayne Parekh"),
    (113, "Aliaksei Protas"),
    (114, "Dylan Cozens"),
    (115, "Alexis Lafreniere"),
    (116, "Sidney Crosby"),
    (117, "J.T. Miller"),
    (118, "Matthew Beniers"),
    (119, "Mason McTavish"),
    (120, "Timo Meier"),
    (121, "Owen Tippett"),
    (122, "Yaroslav Askarov"),
    (123, "Berkly Catton"),
    (124, "Nick Schmaltz"),
    (125, "Darren Raddysh"),
    (126, "Linus Ullmark"),
    (127, "Joey Daccord"),
    (128, "Dylan Strome"),
    (129, "Joel Eriksson Ek"),
    (130, "Anton Lundell"),
    (131, "Troy Terry"),
    (132, "Frank Nazar"),
    (133, "Shea Theodore"),
    (134, "Igor Chernyshov"),
    (135, "Mark Stone"),
    (136, "Carter Verhaeghe"),
    (137, "Morgan Geekie"),
    (138, "Gabe Perreault"),
    (139, "Anton Frondell"),
    (140, "Ryan Leonard"),
    (141, "Kent Johnson"),
    (142, "Jimmy Snuggerud"),
    (143, "Zeev Buium"),
    (144, "Porter Martone"),
    (145, "Zach Hyman"),
    (146, "Tomas Hertl"),
    (147, "Roman Josi"),
    (148, "Philip Broberg"),
    (149, "Alexander Nikishin"),
    (150, "Vince Dunn"),
    (151, "Jared McCann"),
    (152, "Joshua Norris"),
    (153, "Josh Doan"),
    (154, "Adin Hill"),
    (155, "Victor Hedman"),
    (156, "Sergei Bobrovsky"),
    (157, "Darcy Kuemper"),
    # 158 = draft pick, skip
    (159, "Jake O'Brien"),
    (160, "Cole Hutson"),
    (161, "Ben Kindel"),
    (162, "Matthew Coronato"),
    (163, "Logan Stankoven"),
    (164, "Jackson Blake"),
    (165, "Brock Faber"),
    (166, "Marco Rossi"),
    (167, "Rickard Rakell"),
    (168, "Simon Edvinsson"),
    (169, "John Tavares"),
    (170, "Stuart Skinner"),
    (171, "Thatcher Demko"),
    (172, "Artyom Levshunov"),
    (173, "Pyotr Kochetkov"),
    (174, "Jordan Binnington"),
    (175, "Luke Evangelista"),
    (176, "Shane Wright"),
    (177, "Steven Stamkos"),
    (178, "James Hagens"),
    (179, "Owen Power"),
    (180, "Dmitri Voronkov"),
    (181, "Sam Dickenson"),
    (182, "Ilya Protas"),
    (183, "Nazem Kadri"),
    (184, "Pierre-Luc Dubois"),
    (185, "Ryan Nugent-Hopkins"),
    (186, "Brock Boeser"),
    (187, "Will Cuylle"),
    (188, "Denton Mateychuk"),
    (189, "Vincent Trocheck"),
    (190, "MacKenzie Weegar"),
    (191, "Brock Nelson"),
    (192, "Dougie Hamilton"),
    (193, "Anthony Stolarz"),
    (194, "Jacob Markstrom"),
    (195, "Shayne Gostisbehere"),
    (196, "Kaapo Kakko"),
    (197, "Cole Perfetti"),
    (198, "Tyson Foerster"),
    # 199 = draft pick, skip
    (200, "Valeri Nichushkin"),
    (201, "Bryan Rust"),
    (202, "Pavel Buchnevich"),
    (203, "Jiri Kulich"),
    (204, "Matt Duchene"),
    (205, "Alex Ovechkin"),
    (206, "Tom Wilson"),
    (207, "Alex Laferriere"),
    (208, "Shane Pinto"),
    (209, "Olen Zellweger"),
    (210, "Erik Karlsson"),
    (211, "Caleb Desnoyers"),
    (212, "John Carlson"),
    (213, "Jonathan Huberdeau"),
    (214, "Jake Neighbours"),
    (215, "Jack Quinn"),
    (216, "Connor McMichael"),
    (217, "Sam Rinzel"),
    (218, "Carter Yakemchuk"),
    (219, "Axel Sandin Pellikka"),
    (220, "Marco Kasper"),
    (221, "Zachary Bolduc"),
    (222, "Logan Mailloux"),
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

# First pass: classify each entry as skater, goalie, or new player
# then assign sequential ranks within each group
sk_entries = []  # (row_index_or_None, name)
go_entries = []
new_players = []  # (name,) — will default to skaters

for _, name in RANKINGS_RAW:
    key = normalize(name)
    key = NAME_MAP.get(key, key)

    if key in sk_lookup:
        sk_entries.append((sk_lookup[key], name))
    elif key in go_lookup:
        go_entries.append((go_lookup[key], name))
    else:
        # New player — default to skaters (review position after)
        sk_entries.append((None, name))
        new_players.append(name)

# Assign sequential ranks and write into rows
for seq_rank, (row_idx, name) in enumerate(sk_entries, 1):
    if row_idx is not None:
        sk_rows[row_idx][sk_col_idx] = seq_rank
    else:
        new_row = [''] * len(sk_rows[0])
        new_row[0] = name
        new_row[1] = 'F'  # default; verify manually
        new_row[sk_col_idx] = seq_rank
        sk_rows.append(new_row)
        sk_lookup[normalize(name)] = len(sk_rows) - 1

for seq_rank, (row_idx, name) in enumerate(go_entries, 1):
    go_rows[row_idx][go_col_idx] = seq_rank

write_master(SKATERS_PATH, sk_rows)
write_master(GOALIES_PATH, go_rows)

print(f"Skaters: {len(sk_entries) - len(new_players)} matched, {len(new_players)} new")
print(f"Goalies: {len(go_entries)} matched")
if new_players:
    print("\nNew players added to skaters (verify position):")
    for name in new_players:
        print(f"  {name}")

# Recalculate both
for path in [SKATERS_PATH, GOALIES_PATH]:
    subprocess.run(["python3", "scripts/recalculate.py", path], check=True)
    print(f"Recalculated {path}")
