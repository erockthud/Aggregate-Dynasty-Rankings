#!/usr/bin/env python3
"""Update DraftSharks football rankings from Mar 2026 to May 2026."""

import csv
import re
import unicodedata
import subprocess

MASTER_PATH = "football/football_rankings_master.csv"
OLD_COL = "DraftSharks (DraftSharks, 2026-03)"
NEW_COL = "DraftSharks (DraftSharks, 2026-05)"

# Names are clean (no team code embedded) — only suffix/spelling mismatches need NAME_MAP
NEW_RANKINGS = [
    (1,   "Josh Allen"),
    (2,   "Drake Maye"),
    (3,   "Jayden Daniels"),
    (4,   "Lamar Jackson"),
    (5,   "Joe Burrow"),
    (6,   "Bijan Robinson"),
    (7,   "Ja'Marr Chase"),
    (8,   "Caleb Williams"),
    (9,   "Jahmyr Gibbs"),
    (10,  "Patrick Mahomes"),
    (11,  "Jaxon Smith-Njigba"),
    (12,  "Jeremiyah Love"),
    (13,  "Puka Nacua"),
    (14,  "Justin Herbert"),
    (15,  "Jalen Hurts"),
    (16,  "Justin Jefferson"),
    (17,  "Ashton Jeanty"),
    (18,  "CeeDee Lamb"),
    (19,  "Trevor Lawrence"),
    (20,  "Amon-Ra St. Brown"),
    (21,  "Malik Nabers"),
    (22,  "Omarion Hampton"),
    (23,  "De'Von Achane"),
    (24,  "Drake London"),
    (25,  "Nico Collins"),
    (26,  "Brock Purdy"),
    (27,  "Jonathan Taylor"),
    (28,  "Jaxson Dart"),
    (29,  "Bo Nix"),
    (30,  "Brock Bowers"),
    (31,  "Trey McBride"),
    (32,  "James Cook"),
    (33,  "Tetairoa McMillan"),
    (34,  "George Pickens"),
    (35,  "Dak Prescott"),
    (36,  "Kenneth Walker III"),
    (37,  "TreVeyon Henderson"),
    (38,  "C.J. Stroud"),
    (39,  "Jordan Love"),
    (40,  "Quinshon Judkins"),
    (41,  "Emeka Egbuka"),
    (42,  "Christian McCaffrey"),
    (43,  "Breece Hall"),
    (44,  "Fernando Mendoza"),
    (45,  "Colston Loveland"),
    (46,  "Saquon Barkley"),
    (47,  "Tee Higgins"),
    (48,  "Baker Mayfield"),
    (49,  "Rashee Rice"),
    (50,  "Chris Olave"),
    (51,  "Jared Goff"),
    (52,  "Zay Flowers"),
    (53,  "Tyler Shough"),
    (54,  "Jordyn Tyson"),
    (55,  "Josh Jacobs"),
    (56,  "Kyler Murray"),
    (57,  "Makai Lemon"),
    (58,  "Garrett Wilson"),
    (59,  "Ladd McConkey"),
    (60,  "Jameson Williams"),
    (61,  "Carnell Tate"),
    (62,  "Chase Brown"),
    (63,  "Cameron Ward"),
    (64,  "Sam Darnold"),
    (65,  "Bucky Irving"),
    (66,  "A.J. Brown"),
    (67,  "Jaylen Waddle"),
    (68,  "DeVonta Smith"),
    (69,  "Luther Burden III"),
    (70,  "Kyren Williams"),
    (71,  "Tyler Warren"),
    (72,  "Harold Fannin Jr."),
    (73,  "Malik Willis"),
    (74,  "Jadarian Price"),
    (75,  "Rome Odunze"),
    (76,  "Bryce Young"),
    (77,  "Matthew Stafford"),
    (78,  "Brian Thomas Jr."),
    (79,  "Tucker Kraft"),
    (80,  "Marvin Harrison Jr."),
    (81,  "Cameron Skattebo"),
    (82,  "Daniel Jones"),
    (83,  "Derrick Henry"),
    (84,  "Ricky Pearsall"),
    (85,  "Christian Watson"),
    (86,  "Ty Simpson"),
    (87,  "KC Concepcion"),
    (88,  "Terry McLaurin"),
    (89,  "Jordan Addison"),
    (90,  "RJ Harvey"),
    (91,  "Kyle Pitts"),
    (92,  "D.K. Metcalf"),
    (93,  "Javonte Williams"),
    (94,  "D.J. Moore"),
    (95,  "Sam LaPorta"),
    (96,  "Michael Wilson"),
    (97,  "Travis Etienne"),
    (98,  "Alec Pierce"),
    (99,  "Mike Evans"),
    (100, "Courtland Sutton"),
    (101, "Xavier Worthy"),
    (102, "Davante Adams"),
    (103, "Tua Tagovailoa"),
    (104, "Shedeur Sanders"),
    (105, "Kenyon Sadiq"),
    (106, "Jayden Higgins"),
    (107, "Travis Hunter"),
    (108, "Michael Pittman Jr."),
    (109, "Matthew Golden"),
    (110, "Bhayshul Tuten"),
    (111, "D'Andre Swift"),
    (112, "Omar Cooper Jr."),
    (113, "Khalil Shakir"),
    (114, "Oronde Gadsden II"),
    (115, "Romeo Doubs"),
    (116, "Wan'Dale Robinson"),
    (117, "David Montgomery"),
    (118, "Jakobi Meyers"),
    (119, "Quentin Johnston"),
    (120, "Jaylen Warren"),
    (121, "Dalton Kincaid"),
    (122, "Rhamondre Stevenson"),
    (123, "Blake Corum"),
    (124, "Chuba Hubbard"),
    (125, "Jalen McMillan"),
    (126, "Eli Stowers"),
    (127, "Chris Godwin"),
    (128, "Jake Ferguson"),
    (129, "Denzel Boston"),
    (130, "Parker Washington"),
    (131, "Michael Penix Jr."),
    (132, "J.J. McCarthy"),
    (133, "Tony Pollard"),
    (134, "Kyle Monangai"),
    (135, "Jordan Mason"),
    (136, "George Kittle"),
    (137, "Juwan Johnson"),
    (138, "Zach Charbonnet"),
    (139, "Jayden Reed"),
    (140, "J.K. Dobbins"),
    (141, "Tre Harris"),
    (142, "Rashid Shaheed"),
    (143, "Antonio Williams"),
    (144, "Josh Downs"),
    (145, "Woody Marks"),
    (146, "Kenneth Gainwell"),
    (147, "Jalen Coker"),
    (148, "Germie Bernard"),
    (149, "Jacory Croskey-Merritt"),
    (150, "Isaiah Likely"),
    (151, "Rico Dowdle"),
    (152, "Mark Andrews"),
    (153, "Brenton Strange"),
    (154, "Tyjae Spears"),
    (155, "Braelon Allen"),
    (156, "Brandon Aiyuk"),
    (157, "Dallas Goedert"),
    (158, "Jaylin Noel"),
    (159, "Jonathon Brooks"),
    (160, "Travis Kelce"),
    (161, "Hunter Henry"),
    (162, "Terrance Ferguson"),
    (163, "AJ Barner"),
    (164, "T.J. Hockenson"),
    (165, "Troy Franklin"),
    (166, "Pat Freiermuth"),
    (167, "Elijah Arroyo"),
    (168, "Gunnar Helm"),
    (169, "Dalton Schultz"),
    (170, "Isiah Pacheco"),
    (171, "Chigoziem Okonkwo"),
    (172, "De'Zhaun Stribling"),
    (173, "Kayshon Boutte"),
    (174, "Keon Coleman"),
    (175, "Jack Bech"),
    (176, "Theo Johnson"),
    (177, "Zachariah Branch"),
    (178, "Jacoby Brissett"),
    (179, "Pat Bryant"),
    (180, "Chris Bell"),
    (181, "Chris Rodriguez Jr."),
    (182, "Cade Otton"),
    (183, "David Njoku"),
    (184, "Elijah Sarratt"),
    (185, "Tre Tucker"),
    (186, "Michael Mayer"),
    (187, "Jauan Jennings"),
    (188, "Jerry Jeudy"),
    (189, "Tory Horton"),
    (190, "Elic Ayomanor"),
    (191, "Ja'Kobi Lane"),
    (192, "Deebo Samuel"),
    (193, "Tyrone Tracy Jr."),
    (194, "Dontayvion Wicks"),
    (195, "Ted Hurst III"),
    (196, "Tyler Allgeier"),
    (197, "Keaton Mitchell"),
    (198, "Adonai Mitchell"),
    (199, "Chris Brazzell II"),
    (200, "Brian Robinson Jr."),
]

NAME_MAP = {
    "James Cook":       "James Cook III",
    "Travis Etienne":   "Travis Etienne Jr.",
    "Cameron Ward":     "Cam Ward",
    "Cameron Skattebo": "Cam Skattebo",
}


def normalize(name):
    name = unicodedata.normalize("NFKD", name)
    name = name.encode("ascii", "ignore").decode("ascii")
    name = name.lower()
    name = re.sub(r"\b(jr|sr|ii|iii|iv|v)\b\.?", "", name)
    name = re.sub(r"[^a-z\s]", "", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name


def main():
    rankings = []
    for rank, name in NEW_RANKINGS:
        canonical = NAME_MAP.get(name, name)
        rankings.append((rank, canonical))

    with open(MASTER_PATH, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    header = rows[0]
    data = rows[1:]

    ds_idx = header.index(OLD_COL)
    header[ds_idx] = NEW_COL

    name_to_idx = {normalize(row[0]): i for i, row in enumerate(data)}

    for row in data:
        row[ds_idx] = ""

    matched = 0
    unmatched = []

    for rank, name in rankings:
        norm = normalize(name)
        if norm in name_to_idx:
            data[name_to_idx[norm]][ds_idx] = str(rank)
            matched += 1
        else:
            unmatched.append((rank, name))

    print(f"Matched: {matched}")
    print(f"New players to add: {len(unmatched)}")
    for rank, name in unmatched:
        print(f"  [{rank}] {name}")

    for rank, name in unmatched:
        new_row = [""] * len(header)
        new_row[0] = name
        new_row[ds_idx] = str(rank)
        data.append(new_row)

    with open(MASTER_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)

    print(f"\nWrote {len(data)} rows to {MASTER_PATH}")

    result = subprocess.run(
        ["python3", "scripts/recalculate.py", MASTER_PATH],
        capture_output=True, text=True
    )
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)


if __name__ == "__main__":
    main()
