#!/usr/bin/env python3
"""Update RotoWorld (Eric Cross) baseball rankings from Jan 2026 to May 29 2026."""

import csv
import re
import unicodedata
import subprocess

MASTER_PATH = "baseball/baseball_rankings_master.csv"
OLD_COL = "RotoWorld (Eric Cross, 2026-01-15)"
NEW_COL = "RotoWorld (Eric Cross, 2026-05-29)"

NEW_RANKINGS = [
    (1,   "Bobby Witt Jr.",         "SS",    "KCR", 25.95),
    (2,   "Shohei Ohtani",          "UT/SP", "LAD", 31.90),
    (3,   "Juan Soto",              "OF",    "NYM", 27.59),
    (4,   "Corbin Carroll",         "OF",    "ARI", 25.77),
    (5,   "Elly De La Cruz",        "SS",    "CIN", 24.37),
    (6,   "Paul Skenes",            "SP",    "PIT", 24.00),
    (7,   "Julio Rodriguez",        "OF",    "SEA", 25.41),
    (8,   "Tarik Skubal",           "SP",    "DET", 29.52),
    (9,   "Aaron Judge",            "OF",    "NYY", 34.09),
    (10,  "Ronald Acuna Jr.",       "OF",    "ATL", 28.44),
    (11,  "Konnor Griffin",         "SS",    "PIT", 20.09),
    (12,  "Nick Kurtz",             "1B",    "ATH", 23.21),
    (13,  "Junior Caminero",        "3B",    "TBR", 22.90),
    (14,  "James Wood",             "OF",    "WAS", 23.69),
    (15,  "Yordan Alvarez",         "OF",    "HOU", 28.92),
    (16,  "Kevin McGonigle",        "3B",    "DET", 21.77),
    (17,  "Fernando Tatis Jr.",     "OF",    "SDP", 27.40),
    (18,  "Ben Rice",               "C",     "NYY", 27.26),
    (19,  "Jacob Misiorowski",      "SP",    "MIL", 24.15),
    (20,  "Cristopher Sanchez",     "SP",    "PHI", 29.46),
    (21,  "Jackson Chourio",        "OF",    "MIL", 22.21),
    (22,  "Jose Ramirez",           "3B",    "CLE", 33.70),
    (23,  "Gunnar Henderson",       "SS",    "BAL", 24.91),
    (24,  "CJ Abrams",              "SS",    "WAS", 25.65),
    (25,  "Jordan Walker",          "OF",    "STL", 24.02),
    (26,  "Vladimir Guerrero Jr.",  "1B",    "TOR", 27.20),
    (27,  "Kyle Tucker",            "OF",    "LAD", 29.36),
    (28,  "Chase Burns",            "SP",    "CIN", 23.36),
    (29,  "Brice Turang",           "2B",    "MIL", 26.52),
    (30,  "Roman Anthony",          "OF",    "BOS", 22.04),
    (31,  "Garrett Crochet",        "SP",    "BOS", 26.94),
    (32,  "Yoshinobu Yamamoto",     "SP",    "LAD", 27.78),
    (33,  "Ketel Marte",            "2B",    "ARI", 32.63),
    (34,  "JJ Wetherholt",          "2B",    "STL", 23.71),
    (35,  "Cam Schlittler",         "SP",    "NYY", 25.30),
    (36,  "Francisco Lindor",       "SS",    "NYM", 32.54),
    (37,  "Drake Baldwin",          "C",     "ATL", 25.17),
    (38,  "Sal Stewart",            "1B",    "CIN", 22.47),
    (39,  "Jazz Chisholm Jr.",      "2B",    "NYY", 28.32),
    (40,  "Pete Alonso",            "1B",    "BAL", 31.48),
    (41,  "Bryan Woo",              "SP",    "SEA", 26.33),
    (42,  "Kyle Schwarber",         "UT",    "PHI", 33.23),
    (43,  "Nolan McLean",           "SP",    "NYM", 24.84),
    (44,  "Jesus Made",             "SS",    "MIL", 19.05),
    (45,  "Hunter Brown",           "SP",    "HOU", 27.75),
    (46,  "Shea Langeliers",        "C",     "ATH", 28.53),
    (47,  "Miguel Vargas",          "1B",    "CHW", 26.53),
    (48,  "Logan Gilbert",          "SP",    "SEA", 29.06),
    (49,  "Zach Neto",              "SS",    "LAA", 25.32),
    (50,  "Cole Ragans",            "SP",    "KCR", 28.46),
    (51,  "Wyatt Langford",         "OF",    "TEX", 24.53),
    (52,  "Maikel Garcia",          "2B",    "KCR", 26.23),
    (53,  "Leo De Vries",           "SS",    "ATH", 19.62),
    (54,  "Riley Greene",           "OF",    "DET", 25.66),
    (55,  "Matt Olson",             "1B",    "ATL", 32.17),
    (56,  "Joe Ryan",               "SP",    "MIN", 29.98),
    (57,  "Oneil Cruz",             "OF",    "PIT", 27.65),
    (58,  "Max Fried",              "SP",    "NYY", 32.36),
    (59,  "Samuel Basallo",         "C",     "BAL", 21.79),
    (60,  "Hunter Greene",          "SP",    "CIN", 26.81),
    (61,  "Pete Crow-Armstrong",    "OF",    "CHC", 24.17),
    (62,  "Bryce Harper",           "1B",    "PHI", 33.62),
    (63,  "Cal Raleigh",            "C",     "SEA", 29.50),
    (64,  "Randy Arozarena",        "OF",    "SEA", 31.25),
    (65,  "Cody Bellinger",         "OF",    "NYY", 30.88),
    (66,  "Brent Rooker",           "OF",    "ATH", 31.57),
    (67,  "Eury Perez",             "SP",    "MIA", 23.12),
    (68,  "Andy Pages",             "OF",    "LAD", 25.47),
    (69,  "Trey Yesavage",          "SP",    "TOR", 22.83),
    (70,  "Travis Bazzana",         "2B",    "CLE", 23.75),
    (71,  "Mason Miller",           "RP",    "SDP", 27.76),
    (72,  "George Kirby",           "SP",    "SEA", 28.31),
    (73,  "Josh Naylor",            "1B",    "SEA", 28.93),
    (74,  "Freddy Peralta",         "SP",    "NYM", 29.98),
    (75,  "Josue De Paula",         "OF",    "LAD", 21.01),
    (76,  "Dylan Cease",            "SP",    "TOR", 30.42),
    (77,  "Michael Harris II",      "OF",    "ATL", 25.22),
    (78,  "Spencer Schwellenbach",  "SP",    "ATL", 25.99),
    (79,  "Jesus Luzardo",          "SP",    "PHI", 28.66),
    (80,  "Trea Turner",            "SS",    "PHI", 32.91),
    (81,  "Chase DeLauter",         "OF",    "CLE", 24.63),
    (82,  "Edward Florentino",      "OF",    "PIT", 18.55),
    (83,  "Max Clark",              "OF",    "DET", 21.43),
    (84,  "Logan Webb",             "SP",    "SFG", 29.53),
    (85,  "Rafael Devers",          "1B",    "SFG", 29.59),
    (86,  "Manny Machado",          "3B",    "SDP", 33.90),
    (87,  "Gavin Williams",         "SP",    "CLE", 26.84),
    (88,  "Munetaka Murakami",      "1B",    "CHW", 26.31),
    (89,  "Kade Anderson",          "SP",    "SEA", 21.96),
    (90,  "Mookie Betts",           "SS",    "LAD", 33.64),
    (91,  "William Contreras",      "C",     "MIL", 28.43),
    (92,  "Jackson Merrill",        "OF",    "SDP", 23.11),
    (93,  "Spencer Strider",        "SP",    "ATL", 27.58),
    (94,  "Michael Busch",          "1B",    "CHC", 28.55),
    (95,  "Kyle Bradish",           "SP",    "BAL", 29.71),
    (96,  "Byron Buxton",           "OF",    "MIN", 32.45),
    (97,  "Geraldo Perdomo",        "SS",    "ARI", 26.60),
    (98,  "Corey Seager",           "SS",    "TEX", 32.09),
    (99,  "Austin Riley",           "3B",    "ATL", 29.16),
    (100, "Jeremy Pena",            "SS",    "HOU", 28.68),
    (101, "Payton Tolle",           "SP",    "BOS", 23.57),
    (102, "Tyler Soderstrom",       "1B",    "ATH", 24.51),
    (103, "Jackson Holliday",       "2B",    "BAL", 22.48),
    (104, "Seiya Suzuki",           "OF",    "CHC", 31.78),
    (105, "Nico Hoerner",           "2B",    "CHC", 29.04),
    (106, "Ivan Herrera",           "C",     "STL", 25.99),
    (107, "Michael King",           "SP",    "SDP", 31.01),
    (108, "Mike Sirota",            "OF",    "LAD", 22.92),
    (109, "Tyler Glasnow",          "SP",    "LAD", 32.77),
    (110, "Framber Valdez",         "SP",    "DET", 32.53),
    (111, "Bryce Eldridge",         "1B",    "SFG", 21.60),
    (112, "Willy Adames",           "SS",    "SFG", 30.74),
    (113, "Jarren Duran",           "OF",    "BOS", 29.73),
    (114, "Otto Lopez",             "2B",    "MIA", 27.66),
    (115, "Seth Hernandez",         "SP",    "PIT", 19.99),
    (116, "Jonathan Aranda",        "1B",    "TBR", 28.02),
    (117, "Walker Jenkins",         "OF",    "MIN", 21.26),
    (118, "Kyle Stowers",           "OF",    "MIA", 28.40),
    (119, "Thomas White",           "SP",    "MIA", 21.66),
    (120, "Ozzie Albies",           "2B",    "ATL", 29.39),
    (121, "Zyhir Hope",             "OF",    "LAD", 21.35),
    (122, "Vinnie Pasquantino",     "1B",    "KCR", 28.63),
    (123, "Aidan Miller",           "SS",    "PHI", 21.96),
    (124, "Emmet Sheehan",          "SP",    "LAD", 26.53),
    (125, "Pablo Lopez",            "SP",    "MIN", 30.23),
    (126, "Colt Emerson",           "SS",    "SEA", 20.85),
    (127, "Wilyer Abreu",           "OF",    "BOS", 26.93),
    (128, "Hunter Goodman",         "C",     "COL", 26.64),
    (129, "Chandler Simpson",       "OF",    "TBR", 25.52),
    (130, "Ryan Waldschmidt",       "OF",    "ARI", 23.64),
    (131, "Connelly Early",         "SP",    "BOS", 24.15),
    (132, "Ceddanne Rafaela",       "OF",    "BOS", 25.69),
    (133, "Brandon Nimmo",          "OF",    "TEX", 33.17),
    (134, "Alec Burleson",          "1B",    "STL", 27.51),
    (135, "Jac Caglianone",         "OF",    "KCR", 23.30),
    (136, "Will Smith",             "C",     "LAD", 31.17),
    (137, "Parker Messick",         "SP",    "CLE", 25.59),
    (138, "Christian Yelich",       "OF",    "MIL", 34.48),
    (139, "Rainiel Rodriguez",      "C",     "STL", 19.40),
    (140, "Heliot Ramos",           "OF",    "SFG", 26.72),
    (141, "Adley Rutschman",        "C",     "BAL", 28.31),
    (142, "Colson Montgomery",      "3B",    "CHW", 24.25),
    (143, "Yandy Diaz",             "1B",    "TBR", 34.81),
    (144, "Bo Bichette",            "SS",    "NYM", 28.23),
    (145, "Jhoan Duran",            "RP",    "PHI", 28.39),
    (146, "Bubba Chandler",         "SP",    "PIT", 23.70),
    (147, "Kyle Harrison",          "SP",    "MIL", 24.69),
    (148, "Jacob Wilson",           "SS",    "ATH", 24.16),
    (149, "Sandy Alcantara",        "SP",    "MIA", 30.73),
    (150, "Sebastian Walcott",      "SS",    "TEX", 20.20),
    (151, "Alex Bregman",           "3B",    "CHC", 32.17),
    (152, "Blake Snell",            "SP",    "LAD", 33.48),
    (153, "Luke Keaschall",         "2B",    "MIN", 23.78),
    (154, "Ranger Suarez",          "SP",    "BOS", 30.76),
    (155, "Xavier Edwards",         "2B",    "MIA", 26.80),
    (156, "Taylor Ward",            "OF",    "BAL", 32.46),
    (157, "Jose Soriano",           "SP",    "LAA", 27.60),
    (158, "Mike Trout",             "OF",    "LAA", 34.81),
    (159, "Josh Hader",             "RP",    "HOU", 32.14),
    (160, "Ryan Pepiot",            "SP",    "TBR", 28.77),
    (161, "Jo Adell",               "OF",    "LAA", 27.14),
    (162, "Jakob Marsee",           "OF",    "MIA", 24.92),
    (163, "Carson Benge",           "OF",    "NYM", 23.33),
    (164, "Sam Antonacci",          "2B",    "CHW", 23.30),
    (165, "Bryce Elder",            "SP",    "ATL", 27.02),
    (166, "Carter Jensen",          "C",     "KCR", 22.90),
    (167, "Shota Imanaga",          "SP",    "CHC", 32.74),
    (168, "Edwin Diaz",             "RP",    "LAD", 32.19),
    (169, "Brandon Lowe",           "2B",    "PIT", 31.90),
    (170, "A.J. Ewing",             "2B",    "NYM", 21.77),
    (171, "Nick Pivetta",           "SP",    "SDP", 33.29),
    (172, "Jared Jones",            "SP",    "PIT", 24.79),
    (173, "Ian Happ",               "OF",    "CHC", 31.80),
    (174, "Luis Pena",              "2B",    "MIL", 19.53),
    (175, "Casey Schmitt",          "1B",    "SFG", 27.14),
    (176, "Taj Bradley",            "SP",    "MIN", 25.19),
    (177, "Teoscar Hernandez",      "OF",    "LAD", 33.62),
    (178, "MacKenzie Gore",         "SP",    "TEX", 27.26),
    (179, "Jordan Westburg",        "2B",    "BAL", 27.27),
    (180, "Daylen Lile",            "OF",    "WAS", 23.49),
    (181, "Shane McClanahan",       "SP",    "TBR", 29.08),
    (182, "Drew Rasmussen",         "SP",    "TBR", 30.84),
    (183, "Carlos Rodon",           "SP",    "NYY", 33.47),
    (184, "Cade Horton",            "SP",    "CHC", 24.77),
    (185, "Kazuma Okamoto",         "3B",    "TOR", 29.91),
    (186, "Caleb Bonemer",          "SS",    "CHW", 20.65),
    (187, "Freddie Freeman",        "1B",    "LAD", 36.71),
    (188, "Tatsuya Imai",           "SP",    "HOU", 28.05),
    (189, "Roki Sasaki",            "SP",    "LAD", 24.56),
    (190, "Kris Bubic",             "SP",    "KCR", 28.77),
    (191, "Luis Robert Jr.",        "OF",    "NYM", 28.82),
    (192, "Zack Wheeler",           "SP",    "PHI", 36.00),
    (193, "Andres Munoz",           "RP",    "SEA", 27.36),
    (194, "Logan Henderson",        "SP",    "MIL", 24.23),
    (195, "Eduardo Quintero",       "OF",    "LAD", 20.69),
    (196, "Franklin Arias",         "SS",    "BOS", 20.52),
    (197, "Ryan Weathers",          "SP",    "NYY", 26.45),
    (198, "Kaelen Culpepper",       "SS",    "MIN", 23.41),
    (199, "Tanner Bibee",           "SP",    "CLE", 27.23),
    (200, "Shane Bieber",           "SP",    "TOR", 31.00),
]


def normalize(name):
    name = unicodedata.normalize("NFKD", name)
    name = name.encode("ascii", "ignore").decode("ascii")
    name = name.lower()
    name = re.sub(r"\b(jr|sr|ii|iii|iv|v)\b\.?", "", name)
    name = re.sub(r"[^a-z\s]", "", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name


def main():
    # Build new rankings lookup: normalized_name -> (rank, name, pos, team, age)
    new_lookup = {}
    for rank, name, pos, team, age in NEW_RANKINGS:
        key = normalize(name)
        new_lookup[key] = (rank, name, pos, team, age)

    # Read master
    with open(MASTER_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)
        rows = list(reader)

    # Rename column header
    if OLD_COL in fieldnames:
        idx = fieldnames.index(OLD_COL)
        fieldnames[idx] = NEW_COL
        for row in rows:
            row[NEW_COL] = row.pop(OLD_COL, "")
        print(f"Renamed column: '{OLD_COL}' -> '{NEW_COL}'")
    elif NEW_COL not in fieldnames:
        avg_rank_idx = fieldnames.index("Average Rank")
        fieldnames = fieldnames[:avg_rank_idx] + [NEW_COL] + fieldnames[avg_rank_idx:]
        for row in rows:
            row[NEW_COL] = ""
        print(f"Added new column: '{NEW_COL}'")
    else:
        print(f"Column '{NEW_COL}' already exists — updating in place.")

    # Clear the column for all existing rows (so dropped players get blanked)
    for row in rows:
        row[NEW_COL] = ""

    # Track matched keys
    matched_keys = set()

    # Update existing rows
    for row in rows:
        key = normalize(row["Player"])
        if key in new_lookup:
            rank, _, _, _, age = new_lookup[key]
            row[NEW_COL] = rank
            # Backfill age if blank and source has it
            if not row.get("Age") and age:
                row["Age"] = age
            matched_keys.add(key)

    # Find unmatched new players
    unmatched = []
    for rank, name, pos, team, age in NEW_RANKINGS:
        key = normalize(name)
        if key not in matched_keys:
            unmatched.append((rank, name, pos, team, age))

    print(f"Matched: {len(matched_keys)} players")
    print(f"New players to add: {len(unmatched)}")
    for rank, name, pos, team, age in unmatched:
        print(f"  [{rank}] {name} ({pos}, {team})")

    # Add new rows for unmatched players
    for rank, name, pos, team, age in unmatched:
        new_row = {fn: "" for fn in fieldnames}
        new_row["Player"] = name
        new_row["Position"] = pos
        new_row["Team"] = team
        new_row["Age"] = str(age) if age else ""
        new_row[NEW_COL] = rank
        rows.append(new_row)

    # Write back
    with open(MASTER_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nWrote {len(rows)} rows to {MASTER_PATH}")

    # Recalculate
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
