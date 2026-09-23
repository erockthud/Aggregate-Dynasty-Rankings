"""Update Noah Rubin (Cat) basketball rankings: Jan 2026 -> Aug 2026.
Also backfills blank Team fields from this source's team codes (never
overwrites an already-populated Team).
"""
import csv, io, re, subprocess, unicodedata

MASTER_PATH = "basketball/basketball_rankings_master.csv"
OLD_COL = "Noah Rubin (Cat, Jan 2026)"
NEW_COL = "Noah Rubin (Cat, Aug 2026)"

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
    (7, 'Tyrese Maxey', 'PHI'),
    (8, 'Anthony Edwards', 'MIN'),
    (9, 'Tyrese Haliburton', 'IND'),
    (10, 'Jayson Tatum', 'BOS'),
    (11, 'Cameron Boozer', 'MEM'),
    (12, 'Darryn Peterson', 'UTA'),
    (13, 'Jalen Johnson', 'ATL'),
    (14, 'Scottie Barnes', 'TOR'),
    (15, 'Chet Holmgren', 'OKC'),
    (16, 'Jalen Williams', 'OKC'),
    (17, 'Amen Thompson', 'HOU'),
    (18, 'Evan Mobley', 'CLE'),
    (19, 'Giannis Antetokounmpo', 'MIA'),
    (20, 'Alperen Sengun', 'HOU'),
    (21, 'Dylan Harper', 'SAS'),
    (22, 'Karl-Anthony Towns', 'NYK'),
    (23, 'LaMelo Ball', 'MIN'),
    (24, 'Donovan Mitchell', 'CLE'),
    (25, 'Trey Murphy III', 'NOP'),
    (26, 'Darius Garland', 'LAC'),
    (27, 'Devin Booker', 'PHX'),
    (28, 'Caleb Wilson', 'CHI'),
    (29, 'AJ Dybantsa', 'WAS'),
    (30, 'Deni Avdija', 'POR'),
    (31, 'Trae Young', 'WAS'),
    (32, 'Jamal Murray', 'DEN'),
    (33, 'Desmond Bane', 'ORL'),
    (34, 'Franz Wagner', 'ORL'),
    (35, 'Brandon Miller', 'CHA'),
    (36, 'Lauri Markkanen', 'UTA'),
    (37, 'Jaren Jackson Jr.', 'UTA'),
    (38, 'Kon Knueppel', 'CHA'),
    (39, 'Austin Reaves', 'LAL'),
    (40, 'Derrick White', 'BOS'),
    (41, 'VJ Edgecombe', 'PHI'),
    (42, 'Alex Sarr', 'WAS'),
    (43, 'Jalen Brunson', 'NYK'),
    (44, 'Jaylen Brown', 'PHI'),
    (45, 'Paolo Banchero', 'ORL'),
    (46, 'Kingston Flemings', 'ATL'),
    (47, 'Domantas Sabonis', 'SAC'),
    (48, 'Collin Murray-Boyles', 'TOR'),
    (49, 'Bam Adebayo', 'MIA'),
    (50, 'Anthony Davis', 'WAS'),
    (51, "De'Aaron Fox", 'SAS'),
    (52, 'Dyson Daniels', 'ATL'),
    (53, 'OG Anunoby', 'NYK'),
    (54, 'Mikel Brown', 'BKN'),
    (55, 'Walker Kessler', 'LAL'),
    (56, 'Donovan Clingan', 'POR'),
    (57, 'Zach Edey', 'MEM'),
    (58, 'Stephon Castle', 'SAS'),
    (59, "Kel'el Ware", 'MIL'),
    (60, 'Jalen Duren', 'DET'),
    (61, 'Darius Acuff Jr.', 'Arkansas'),
    (62, 'Keaton Wagler', 'LAC'),
    (63, 'Ausar Thompson', 'DET'),
    (64, 'Onyeka Okongwu', 'ATL'),
    (65, 'Keyonte George', 'UTA'),
    (66, 'Kyshawn George', 'WAS'),
    (67, 'Ace Bailey', 'UTA'),
    (68, 'Kyrie Irving', 'DAL'),
    (69, 'James Harden', 'CLE'),
    (70, 'Mikal Bridges', 'NYK'),
    (71, 'Stephen Curry', 'GSW'),
    (72, 'Kevin Durant', 'HOU'),
    (73, 'Ja Morant', 'POR'),
    (74, 'Kawhi Leonard', 'TOR'),
    (75, 'Jalen Suggs', 'ORL'),
    (76, 'Zion Williamson', 'NOP'),
    (77, 'Derik Queen', 'NOP'),
    (78, 'Dejounte Murray', 'NOP'),
    (79, 'Reed Sheppard', 'HOU'),
    (80, 'Ivica Zubac', 'IND'),
    (81, 'Pascal Siakam', 'IND'),
    (82, 'Brandon Ingram', 'LAC'),
    (83, 'Scoot Henderson', 'POR'),
    (84, 'Jaden McDaniels', 'MIN'),
    (85, 'Ryan Rollins', 'MIL'),
    (86, 'Egor Dëmin', 'BKN'),
    (87, 'Ajay Mitchell', 'OKC'),
    (88, 'Josh Giddey', 'CHI'),
    (89, 'Matas Buzelis', 'CHI'),
    (90, 'Coby White', 'CHA'),
    (91, 'Payton Pritchard', 'BOS'),
    (92, 'Nickeil Alexander-Walker', 'ATL'),
    (93, 'Cedric Coward', 'MEM'),
    (94, 'Immanuel Quickley', 'TOR'),
    (95, 'Devin Vassell', 'SAS'),
    (96, 'Jarrett Allen', 'CLE'),
    (97, 'Jeremiah Fears', 'NOP'),
    (98, 'Tyler Herro', 'MIL'),
    (99, 'Tari Eason', 'HOU'),
    (100, 'Naz Reid', 'CHA'),
    (101, 'Peyton Watson', 'CLE'),
    (102, 'Jabari Smith Jr.', 'HOU'),
    (103, 'Andrew Nembhard', 'IND'),
    (104, 'Morez Johnson', 'DAL'),
    (105, 'Jimmy Butler III', 'GSW'),
    (106, 'Kristaps Porziņģis', 'GSW'),
    (107, 'Brayden Burries', 'MIL'),
    (108, 'Anthony Black', 'ORL'),
    (109, 'Jalen Green', 'PHX'),
    (110, 'Cason Wallace', 'OKC'),
    (111, 'Yaxel Lendeborg', 'GSW'),
    (112, 'Michael Porter Jr.', 'BKN'),
    (113, 'Josh Hart', 'NYK'),
    (114, 'Nic Claxton', 'CHI'),
    (115, 'P.J. Washington', 'DAL'),
    (116, 'Dereck Lively II', 'DAL'),
    (117, 'Norman Powell', 'CHI'),
    (118, 'LeBron James', 'PHI'),
    (119, 'Quentin Grimes', 'LAL'),
    (120, 'Brandin Podziemski', 'GSW'),
    (121, 'Santi Aldama', 'DAL'),
    (122, 'Jaylon Tyson', 'CLE'),
    (123, 'Ty Jerome', 'MEM'),
    (124, 'Julius Randle', 'BKN'),
    (125, 'Paul George', 'BOS'),
    (126, 'Dailyn Swain', 'CHI'),
    (127, 'Hugo González', 'BOS'),
    (128, 'Neemias Queta', 'BOS'),
    (129, 'Mitchell Robinson', 'BOS'),
    (130, 'Christian Anderson', 'CHA'),
    (131, 'Hannes Steinbach', 'CHA'),
    (132, 'Aday Mara', 'OKC'),
    (133, 'Moussa Diabaté', 'CHA'),
    (134, 'Bennett Stirtz', 'OKC'),
    (135, 'Ebuka Okorie', 'DET'),
    (136, 'Allen Graves', 'TOR'),
    (137, 'Thomas Sorber', 'OKC'),
    (138, 'Khaman Maluach', 'PHX'),
    (139, 'Keegan Murray', 'SAC'),
    (140, 'Kyle Filipowski', 'UTA'),
    (141, 'Ronald Holland II', 'DET'),
    (142, 'Tre Johnson', 'WAS'),
    (143, 'Bilal Coulibaly', 'WAS'),
    (144, 'Zach LaVine', 'SAC'),
    (145, 'Toumani Camara', 'POR'),
    (146, 'Rudy Gobert', 'MIN'),
    (147, 'Joel Embiid', 'PHI'),
    (148, 'Collin Gillespie', 'PHX'),
    (149, 'Yang Hansen', 'POR'),
    (150, 'Maxime Raynaud', 'SAC'),
    (151, 'Labaron Philon', 'PHI'),
    (152, 'Carter Bryant', 'SAS'),
    (153, 'Will Riley', 'WAS'),
    (154, 'Brice Sensabaugh', 'UTA'),
    (155, 'Donte DiVincenzo', 'MIN'),
    (156, 'Myles Turner', 'MIL'),
    (157, 'Kasparas Jakučionis', 'MIL'),
    (158, 'Mark Williams', 'PHX'),
    (159, 'Isaiah Hartenstein', 'OKC'),
    (160, 'Oso Ighodaro', 'PHX'),
    (161, 'Herbert Jones', 'NOP'),
    (162, 'Joan Beringer', 'MIN'),
    (163, "Day'Ron Sharpe", 'BKN'),
    (164, 'Naji Marshall', 'DAL'),
    (165, 'Cameron Johnson', 'DEN'),
    (166, 'Christian Braun', 'DEN'),
    (167, 'Zuby Ejiofor', 'ATL'),
    (168, 'Jordan Walsh', 'BOS'),
    (169, 'Cameron Carr', 'LAL'),
    (170, 'Davion Mitchell', 'MIA'),
    (171, 'Miles Bridges', 'PHX'),
    (172, 'Wendell Carter Jr.', 'ORL'),
    (173, 'Isaiah Collier', 'UTA'),
    (174, 'Jakob Poeltl', 'TOR'),
    (175, 'Julian Champagnie', 'SAS'),
    (176, 'Nique Clifford', 'SAC'),
    (177, 'Damian Lillard', 'POR'),
    (178, 'Nikola Topić', 'OKC'),
    (179, 'Goga Bitadze', 'ORL'),
    (180, 'Moses Moody', 'GSW'),
    (181, 'Aaron Nesmith', 'IND'),
    (182, 'Jarace Walker', 'IND'),
    (183, 'John Collins', 'DET'),
    (184, 'Paul Reed', 'DET'),
    (185, 'Fred VanVleet', 'HOU'),
    (186, 'Draymond Green', 'GSW'),
    (187, 'Ayo Dosunmu', 'MIN'),
    (188, 'Bennedict Mathurin', 'NOP'),
    (189, 'Yanic Konan Niederhäuser', 'LAC'),
    (190, 'Grayson Allen', 'CHA'),
    (191, 'Kelly Oubre Jr.', 'IND'),
    (192, 'Gui Santos', 'GSW'),
    (193, 'Daniss Jenkins', 'DET'),
    (194, 'Obi Toppin', 'IND'),
    (195, 'Daniel Gafford', 'DAL'),
    (196, 'Tre Jones', 'CHI'),
    (197, 'Max Strus', 'LAC'),
    (198, 'CJ McCollum', 'ATL'),
    (199, 'Max Christie', 'DAL'),
    (200, "De'Anthony Melton", 'GSW'),
    (201, 'Rui Hachimura', 'LAC'),
    (202, 'Sandro Mamukelashvili', 'LAL'),
    (203, 'Bruce Thornton', 'HOU'),
    (204, 'Karim Lopez', 'MEM'),
    (205, 'Aaron Gordon', 'DEN'),
    (206, 'Baba Miller', 'LAC'),
    (207, 'Nate Ament', 'MIL'),
    (208, 'Scotty Pippen Jr.', 'MEM'),
    (209, 'Noa Essengue', 'CHI'),
    (210, 'Craig Porter Jr.', 'CLE'),
    (211, 'Noah Clowney', 'BKN'),
    (212, 'Jonathan Kuminga', 'MIN'),
    (213, 'Andrew Wiggins', 'MIA'),
    (214, 'Jayden Quaintance', 'SAS'),
    (215, 'Asa Newell', 'ATL'),
    (216, 'Malik Monk', 'SAC'),
    (217, 'Miles McBride', 'NYK'),
    (218, 'Anfernee Simons', 'PHI'),
    (219, 'Noah Penda', 'ORL'),
    (220, 'Jay Huff', 'IND'),
    (221, 'Jared McCain', 'OKC'),
    (222, 'Ousmane Dieng', 'MIL'),
    (223, 'Rasheer Fleming', 'PHX'),
    (224, 'Ryan Dunn', 'PHX'),
    (225, 'Walter Clayton Jr.', 'MEM'),
    (226, 'Collin Sexton', 'LAL'),
    (227, 'Jake LaRavia', 'LAL'),
    (228, 'Adou Thiero', 'LAL'),
    (229, 'Dylan Cardwell', 'SAC'),
    (230, 'Jrue Holiday', 'POR'),
    (231, 'Shaedon Sharpe', 'POR'),
    (232, 'Isaiah Jackson', 'LAC'),
    (233, 'Jamal Shead', 'TOR'),
    (234, 'Tarris Reed', 'SAS'),
    (235, 'Jase Richardson', 'ORL'),
    (236, 'Sergio De Larrea', 'DAL'),
    (237, 'GG Jackson', 'MEM'),
    (238, 'Jordan Poole', 'NOP'),
    (239, 'Saddiq Bey', 'NOP'),
    (240, 'Danny Wolf', 'BKN'),
    (241, 'Keon Ellis', 'BKN'),
    (242, 'Baylor Scheierman', 'BOS'),
    (243, 'Josh Minott', 'BKN'),
    (244, 'Yves Missi', 'NOP'),
    (245, 'Kevin Porter Jr.', 'MIL'),
    (246, 'Jaime Jaquez Jr.', 'MIL'),
    (247, 'Jonathan Mogbo', 'SAC'),
    (248, 'Robert Williams III', 'POR'),
    (249, 'Jalen Smith', 'CHI'),
    (250, 'Leonard Miller', 'CHI'),
]

with open(MASTER_PATH, newline='', encoding='utf-8') as f:
    rows = list(csv.reader(f))

header = rows[0]
col_idx = header.index(OLD_COL)
team_idx = header.index('Team')
header[col_idx] = NEW_COL

lookup = {}
for i, row in enumerate(rows[1:], 1):
    if row:
        lookup[normalize(row[0])] = i

for row in rows[1:]:
    if len(row) > col_idx:
        row[col_idx] = ''

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
        unmatched.append((rank, name, team))

out = io.StringIO()
csv.writer(out).writerows(rows)
with open(MASTER_PATH, 'w', newline='', encoding='utf-8') as f:
    f.write(out.getvalue())

print(f"Matched/updated: {matched}")
print(f"Team backfilled: {team_backfilled}")
print(f"Unmatched: {len(unmatched)}")
for rank, name, team in unmatched:
    print(f"  {rank}\t{name}\t{team}")

subprocess.run(["python3", "scripts/recalculate.py", MASTER_PATH], check=True)
print(f"Recalculated {MASTER_PATH}")
