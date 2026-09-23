"""Add Zach Reifschneider (Cat, Aug 2026) basketball rankings as a new source.
Backfills blank Team fields from this source's team codes (never
overwrites an already-populated Team).
"""
import csv, io, re, subprocess, unicodedata

MASTER_PATH = "basketball/basketball_rankings_master.csv"
NEW_COL = "Zach Reifschneider (Cat, Aug 2026)"

def normalize(name):
    name = unicodedata.normalize("NFKD", name)
    name = name.encode("ascii", "ignore").decode("ascii")
    name = name.lower()
    name = re.sub(r"\b(jr|sr|ii|iii|iv|v)\b\.?", "", name)
    name = re.sub(r"[^a-z\s]", "", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name

# Known basketball canonical-name conventions
NAME_MAP = {
    "alexandre sarr": "alex sarr",
    "carlton carrington": "bub carrington",
    "ron holland": "ronald holland",
    "nicolas claxton": "nic claxton",
}

# (rank, name, team)
RANKINGS = [
    (1, 'Victor Wembanyama', 'SAS'),
    (2, 'Shai Gilgeous-Alexander', 'OKC'),
    (3, 'Luka Dončić', 'LAL'),
    (4, 'Nikola Jokić', 'DEN'),
    (5, 'Cooper Flagg', 'DAL'),
    (6, 'Cade Cunningham', 'DET'),
    (7, 'Jayson Tatum', 'BOS'),
    (8, 'Anthony Edwards', 'MIN'),
    (9, 'Tyrese Maxey', 'PHI'),
    (10, 'Jalen Johnson', 'ATL'),
    (11, 'Tyrese Haliburton', 'IND'),
    (12, 'Cameron Boozer', 'MEM'),
    (13, 'Scottie Barnes', 'TOR'),
    (14, 'Alperen Sengun', 'HOU'),
    (15, 'Darryn Peterson', 'UTA'),
    (16, 'Chet Holmgren', 'OKC'),
    (17, 'Giannis Antetokounmpo', 'MIA'),
    (18, 'AJ Dybantsa', 'WAS'),
    (19, 'Evan Mobley', 'CLE'),
    (20, 'Dylan Harper', 'SAS'),
    (21, 'Amen Thompson', 'HOU'),
    (22, 'Jalen Williams', 'OKC'),
    (23, 'Austin Reaves', 'LAL'),
    (24, 'Franz Wagner', 'ORL'),
    (25, 'Donovan Mitchell', 'CLE'),
    (26, 'Josh Giddey', 'CHI'),
    (27, 'Kon Knueppel', 'CHA'),
    (28, 'Caleb Wilson', 'CHI'),
    (29, 'Deni Avdija', 'POR'),
    (30, 'Darius Garland', 'LAC'),
    (31, 'Jamal Murray', 'DEN'),
    (32, 'LaMelo Ball', 'MIN'),
    (33, 'Jalen Brunson', 'NYK'),
    (34, 'Jalen Duren', 'DET'),
    (35, 'Devin Booker', 'PHX'),
    (36, 'Trey Murphy III', 'NOP'),
    (37, 'Karl-Anthony Towns', 'NYK'),
    (38, 'Paolo Banchero', 'ORL'),
    (39, 'Jaren Jackson Jr.', 'UTA'),
    (40, 'Jaylen Brown', 'PHI'),
    (41, 'Trae Young', 'WAS'),
    (42, 'Bam Adebayo', 'MIA'),
    (43, 'VJ Edgecombe', 'PHI'),
    (44, 'Stephon Castle', 'SAS'),
    (45, 'Brandon Miller', 'CHA'),
    (46, 'Donovan Clingan', 'POR'),
    (47, 'Alex Sarr', 'WAS'),
    (48, 'Lauri Markkanen', 'UTA'),
    (49, 'Zach Edey', 'MEM'),
    (50, 'Desmond Bane', 'ORL'),
    (51, 'Keyonte George', 'UTA'),
    (52, 'Keaton Wagler', 'LAC'),
    (53, 'Onyeka Okongwu', 'ATL'),
    (54, 'Walker Kessler', 'LAL'),
    (55, 'Ivica Zubac', 'IND'),
    (56, 'Mikel Brown', 'BKN'),
    (57, 'Brandon Ingram', 'LAC'),
    (58, "Kel'el Ware", 'MIL'),
    (59, 'Domantas Sabonis', 'SAC'),
    (60, 'James Harden', 'CLE'),
    (61, 'Kevin Durant', 'HOU'),
    (62, "De'Aaron Fox", 'SAS'),
    (63, 'Stephen Curry', 'GSW'),
    (64, 'Anthony Davis', 'WAS'),
    (65, 'OG Anunoby', 'NYK'),
    (66, 'Darius Acuff Jr.', 'Arkansas'),
    (67, 'Derrick White', 'BOS'),
    (68, 'Matas Buzelis', 'CHI'),
    (69, 'Zion Williamson', 'NOP'),
    (70, 'Pascal Siakam', 'IND'),
    (71, 'Collin Murray-Boyles', 'TOR'),
    (72, 'Tyler Herro', 'MIL'),
    (73, 'Jaden McDaniels', 'MIN'),
    (74, 'Jalen Suggs', 'ORL'),
    (75, 'Kyrie Irving', 'DAL'),
    (76, 'Dyson Daniels', 'ATL'),
    (77, 'Kawhi Leonard', 'TOR'),
    (78, 'Kingston Flemings', 'ATL'),
    (79, 'Cedric Coward', 'MEM'),
    (80, 'Ryan Rollins', 'MIL'),
    (81, 'Joel Embiid', 'PHI'),
    (82, 'Ja Morant', 'POR'),
    (83, 'Kyshawn George', 'WAS'),
    (84, 'Jarrett Allen', 'CLE'),
    (85, 'Ausar Thompson', 'DET'),
    (86, 'Reed Sheppard', 'HOU'),
    (87, 'Isaiah Hartenstein', 'OKC'),
    (88, 'Nickeil Alexander-Walker', 'ATL'),
    (89, 'Derik Queen', 'NOP'),
    (90, 'Mikal Bridges', 'NYK'),
    (91, 'Morez Johnson', 'DAL'),
    (92, 'Coby White', 'CHA'),
    (93, 'Scoot Henderson', 'POR'),
    (94, 'Ace Bailey', 'UTA'),
    (95, 'Payton Pritchard', 'BOS'),
    (96, 'Nic Claxton', 'CHI'),
    (97, 'Michael Porter Jr.', 'BKN'),
    (98, 'Naz Reid', 'CHA'),
    (99, 'Tari Eason', 'HOU'),
    (100, 'Peyton Watson', 'CLE'),
    (101, 'Immanuel Quickley', 'TOR'),
    (102, 'Ajay Mitchell', 'OKC'),
    (103, 'Egor Dëmin', 'BKN'),
    (104, 'Aday Mara', 'OKC'),
    (105, 'Julius Randle', 'BKN'),
    (106, 'Anthony Black', 'ORL'),
    (107, 'Brayden Burries', 'MIL'),
    (108, 'Jalen Green', 'PHX'),
    (109, 'Jeremiah Fears', 'NOP'),
    (110, 'Joan Beringer', 'MIN'),
    (111, 'Mark Williams', 'PHX'),
    (112, 'Keegan Murray', 'SAC'),
    (113, 'Jabari Smith Jr.', 'HOU'),
    (114, 'Dejounte Murray', 'NOP'),
    (115, 'Miles Bridges', 'PHX'),
    (116, 'Cason Wallace', 'OKC'),
    (117, 'Zach LaVine', 'SAC'),
    (118, 'Yaxel Lendeborg', 'GSW'),
    (119, 'Andrew Nembhard', 'IND'),
    (120, 'Josh Hart', 'NYK'),
    (121, 'Khaman Maluach', 'PHX'),
    (122, 'Devin Vassell', 'SAS'),
    (123, 'Myles Turner', 'MIL'),
    (124, "Day'Ron Sharpe", 'BKN'),
    (125, 'Toumani Camara', 'POR'),
    (126, 'Ebuka Okorie', 'DET'),
    (127, 'Paul George', 'BOS'),
    (128, 'Tre Johnson', 'WAS'),
    (129, 'Carter Bryant', 'SAS'),
    (130, 'P.J. Washington', 'DAL'),
    (131, 'Shaedon Sharpe', 'POR'),
    (132, 'Norman Powell', 'CHI'),
    (133, 'Jakob Poeltl', 'TOR'),
    (134, 'Dailyn Swain', 'CHI'),
    (135, 'Hannes Steinbach', 'CHA'),
    (136, 'Rudy Gobert', 'MIN'),
    (137, 'Kristaps Porziņģis', 'GSW'),
    (138, 'Ty Jerome', 'MEM'),
    (139, 'Bennett Stirtz', 'OKC'),
    (140, 'Fred VanVleet', 'HOU'),
    (141, 'Santi Aldama', 'DAL'),
    (142, 'John Collins', 'DET'),
    (143, 'Aaron Gordon', 'DEN'),
    (144, 'Neemias Queta', 'BOS'),
    (145, 'Thomas Sorber', 'OKC'),
    (146, 'LeBron James', 'PHI'),
    (147, 'Jared McCain', 'OKC'),
    (148, 'Jaime Jaquez Jr.', 'MIL'),
    (149, 'Bilal Coulibaly', 'WAS'),
    (150, 'Dereck Lively II', 'DAL'),
    (151, 'Maxime Raynaud', 'SAC'),
    (152, 'Ronald Holland II', 'DET'),
    (153, 'Christian Anderson', 'CHA'),
    (154, 'Daniel Gafford', 'DAL'),
    (155, 'RJ Barrett', 'TOR'),
    (156, 'Jaylon Tyson', 'CLE'),
    (157, 'Deandre Ayton', 'WAS'),
    (158, 'Ayo Dosunmu', 'MIN'),
    (159, 'Moussa Diabaté', 'CHA'),
    (160, 'Damian Lillard', 'POR'),
    (161, 'Brandin Podziemski', 'GSW'),
    (162, 'Aaron Nesmith', 'IND'),
    (163, 'Naji Marshall', 'DAL'),
    (164, 'Christian Braun', 'DEN'),
    (165, 'Hugo González', 'BOS'),
    (166, 'Quentin Grimes', 'LAL'),
    (167, 'Will Riley', 'WAS'),
    (168, 'Kasparas Jakučionis', 'MIL'),
    (169, 'Cameron Carr', 'LAL'),
    (170, 'Allen Graves', 'TOR'),
    (171, 'Andrew Wiggins', 'MIA'),
    (172, 'Isaiah Stewart', 'MEM'),
    (173, 'Collin Gillespie', 'PHX'),
    (174, 'Julian Champagnie', 'SAS'),
    (175, 'Mitchell Robinson', 'BOS'),
    (176, 'Jonathan Kuminga', 'MIN'),
    (177, 'Wendell Carter Jr.', 'ORL'),
    (178, 'Noa Essengue', 'CHI'),
    (179, 'Labaron Philon', 'PHI'),
    (180, 'Nate Ament', 'MIL'),
    (181, 'Dillon Brooks', 'PHX'),
    (182, 'Kevin Porter Jr.', 'MIL'),
    (183, 'Herbert Jones', 'NOP'),
    (184, 'Max Christie', 'DAL'),
    (185, 'Davion Mitchell', 'MIA'),
    (186, 'Gui Santos', 'GSW'),
    (187, 'Cameron Johnson', 'DEN'),
    (188, 'Kyle Filipowski', 'UTA'),
    (189, 'Malik Monk', 'SAC'),
    (190, 'Karim Lopez', 'MEM'),
    (191, 'Nikola Topić', 'OKC'),
    (192, 'Noah Penda', 'ORL'),
    (193, 'Jimmy Butler III', 'GSW'),
    (194, 'CJ McCollum', 'ATL'),
    (195, 'Paul Reed', 'DET'),
    (196, 'Jamal Shead', 'TOR'),
    (197, 'Bennedict Mathurin', 'NOP'),
    (198, 'Daniss Jenkins', 'DET'),
    (199, 'Draymond Green', 'GSW'),
    (200, 'Danny Wolf', 'BKN'),
    (201, 'Sergio De Larrea', 'DAL'),
    (202, 'Jayden Quaintance', 'SAS'),
    (203, 'Tarris Reed', 'SAS'),
    (204, 'Jrue Holiday', 'POR'),
    (205, 'Sandro Mamukelashvili', 'LAL'),
    (206, 'Josh Minott', 'BKN'),
    (207, 'Kobe Sanders', 'LAC'),
    (208, 'Walter Clayton Jr.', 'MEM'),
    (209, 'Grayson Allen', 'CHA'),
    (210, 'Nique Clifford', 'SAC'),
    (211, 'Scotty Pippen Jr.', 'MEM'),
    (212, 'Aaron Wiggins', 'ATL'),
    (213, 'Nolan Traore', 'BKN'),
    (214, 'Cam Spencer', 'MEM'),
    (215, 'Koa Peat', 'PHX'),
    (216, 'Terrence Shannon Jr.', 'MIN'),
    (217, 'Tre Jones', 'CHI'),
    (218, 'Bobby Portis', 'MIA'),
    (219, "De'Andre Hunter", 'SAC'),
    (220, 'Robert Williams III', 'POR'),
    (221, 'Jaylen Wells', 'MEM'),
    (222, 'Rui Hachimura', 'LAC'),
    (223, 'Tobias Harris', 'SAS'),
    (224, 'Sam Hauser', 'BOS'),
    (225, 'Jerami Grant', 'MEM'),
    (226, 'Anfernee Simons', 'PHI'),
    (227, 'Bruce Thornton', 'HOU'),
    (228, 'Chris Cenac', 'BOS'),
    (229, 'Zuby Ejiofor', 'ATL'),
    (230, 'Joshua Jefferson', 'BKN'),
    (231, 'Justin Champagnie', 'WAS'),
    (232, 'Ousmane Dieng', 'MIL'),
    (233, "De'Anthony Melton", 'GSW'),
    (234, 'Rob Dillingham', 'CHI'),
    (235, 'Zaccharie Risacher', 'DAL'),
    (236, 'DeMar DeRozan', 'DEN'),
    (237, 'Saddiq Bey', 'NOP'),
    (238, 'Jordan Poole', 'NOP'),
    (239, 'Jusuf Nurkić', 'UTA'),
    (240, 'Dylan Cardwell', 'SAC'),
    (241, 'Isaiah Collier', 'UTA'),
    (242, 'Yanic Konan Niederhäuser', 'LAC'),
    (243, 'Nikola Vučević', 'ORL'),
    (244, 'Ryan Kalkbrenner', 'CHA'),
    (245, 'Tristan da Silva', 'ORL'),
    (246, 'Meleek Thomas', 'CLE'),
    (247, 'Collin Sexton', 'LAL'),
    (248, 'Donte DiVincenzo', 'MIN'),
    (249, 'Sam Merrill', 'CLE'),
    (250, 'Pelle Larsson', 'MIA'),
]

with open(MASTER_PATH, newline='', encoding='utf-8') as f:
    rows = list(csv.reader(f))

header = rows[0]
avg_idx = header.index('Average Rank')
team_idx = header.index('Team')

for row in rows:
    if len(row) >= avg_idx:
        row.insert(avg_idx, '')
header[avg_idx] = NEW_COL
col_idx = avg_idx

lookup = {}
for i, row in enumerate(rows[1:], 1):
    if row:
        lookup[normalize(row[0])] = i

matched = 0
unmatched = []
team_backfilled = 0

for rank, name, team in RANKINGS:
    key = normalize(name)
    key = NAME_MAP.get(key, key)
    if key in lookup:
        row_idx = lookup[key]
        rows[row_idx][col_idx] = rank
        matched += 1
        if not rows[row_idx][team_idx].strip() and team:
            rows[row_idx][team_idx] = team
            team_backfilled += 1
    else:
        new_row = [''] * len(header)
        new_row[0] = name
        new_row[team_idx] = team
        new_row[col_idx] = rank
        rows.append(new_row)
        lookup[key] = len(rows) - 1
        unmatched.append((rank, name, team))

out = io.StringIO()
csv.writer(out).writerows(rows)
with open(MASTER_PATH, 'w', newline='', encoding='utf-8') as f:
    f.write(out.getvalue())

print(f"Matched/updated: {matched}")
print(f"Team backfilled: {team_backfilled}")
print(f"New players added: {len(unmatched)}")
for rank, name, team in unmatched:
    print(f"  {rank}\t{name}\t{team}")

subprocess.run(["python3", "scripts/recalculate.py", MASTER_PATH], check=True)
print(f"Recalculated {MASTER_PATH}")
