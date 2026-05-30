#!/usr/bin/env python3
"""Update FantasyPros football rankings from Mar 2026 to May 2026."""

import csv
import re
import unicodedata
import subprocess

MASTER_PATH = "football/football_rankings_master.csv"
OLD_COL = "FantasyPros (FantasyPros, 2026-03)"
NEW_COL = "FantasyPros (FantasyPros, 2026-05)"

# Names are formatted "Player Name (TEAM)" — team stripped by strip_team()
# Sr./Jr./II/III suffixes handled by normalize(); no manual cleanup needed for those.
RAW = [
    (1,   "Josh Allen (BUF)"),
    (2,   "Drake Maye (NE)"),
    (3,   "Jayden Daniels (WAS)"),
    (4,   "Ja'Marr Chase (CIN)"),
    (5,   "Lamar Jackson (BAL)"),
    (6,   "Jaxon Smith-Njigba (SEA)"),
    (7,   "Joe Burrow (CIN)"),
    (8,   "Puka Nacua (LAR)"),
    (9,   "Caleb Williams (CHI)"),
    (10,  "Patrick Mahomes II (KC)"),
    (11,  "Bijan Robinson (ATL)"),
    (12,  "Jahmyr Gibbs (DET)"),
    (13,  "Justin Herbert (LAC)"),
    (14,  "Justin Jefferson (MIN)"),
    (15,  "Jalen Hurts (PHI)"),
    (16,  "CeeDee Lamb (DAL)"),
    (17,  "Amon-Ra St. Brown (DET)"),
    (18,  "Malik Nabers (NYG)"),
    (19,  "Ashton Jeanty (LV)"),
    (20,  "Trevor Lawrence (JAC)"),
    (21,  "Jaxson Dart (NYG)"),
    (22,  "Jeremiyah Love (ARI)"),
    (23,  "Drake London (ATL)"),
    (24,  "Brock Purdy (SF)"),
    (25,  "Bo Nix (DEN)"),
    (26,  "De'Von Achane (MIA)"),
    (27,  "Tetairoa McMillan (CAR)"),
    (28,  "Omarion Hampton (LAC)"),
    (29,  "Brock Bowers (LV)"),
    (30,  "James Cook III (BUF)"),
    (31,  "Nico Collins (HOU)"),
    (32,  "Jonathan Taylor (IND)"),
    (33,  "Jordan Love (GB)"),
    (34,  "George Pickens (DAL)"),
    (35,  "Emeka Egbuka (TB)"),
    (36,  "Trey McBride (ARI)"),
    (37,  "Dak Prescott (DAL)"),
    (38,  "Chris Olave (NO)"),
    (39,  "Garrett Wilson (NYJ)"),
    (40,  "Carnell Tate (TEN)"),
    (41,  "Kenneth Walker III (KC)"),
    (42,  "Ladd McConkey (LAC)"),
    (43,  "Breece Hall (NYJ)"),
    (44,  "Rashee Rice (KC)"),
    (45,  "A.J. Brown (PHI)"),
    (46,  "Jordyn Tyson (NO)"),
    (47,  "DeVonta Smith (PHI)"),
    (48,  "Colston Loveland (CHI)"),
    (49,  "Luther Burden III (CHI)"),
    (50,  "Makai Lemon (PHI)"),
    (51,  "Tee Higgins (CIN)"),
    (52,  "Fernando Mendoza (LV)"),
    (53,  "Baker Mayfield (TB)"),
    (54,  "Rome Odunze (CHI)"),
    (55,  "Chase Brown (CIN)"),
    (56,  "Zay Flowers (BAL)"),
    (57,  "Tyler Warren (IND)"),
    (58,  "C.J. Stroud (HOU)"),
    (59,  "TreVeyon Henderson (NE)"),
    (60,  "Jared Goff (DET)"),
    (61,  "Jaylen Waddle (DEN)"),
    (62,  "Christian McCaffrey (SF)"),
    (63,  "Marvin Harrison Jr. (ARI)"),
    (64,  "Cam Ward (TEN)"),
    (65,  "Saquon Barkley (PHI)"),
    (66,  "Tucker Kraft (GB)"),
    (67,  "Harold Fannin Jr. (CLE)"),
    (68,  "Jameson Williams (DET)"),
    (69,  "Brian Thomas Jr. (JAC)"),
    (70,  "Quinshon Judkins (CLE)"),
    (71,  "Sam LaPorta (DET)"),
    (72,  "Bucky Irving (TB)"),
    (73,  "Tyler Shough (NO)"),
    (74,  "Travis Etienne Jr. (NO)"),
    (75,  "Kyler Murray (MIN)"),
    (76,  "Kyren Williams (LAR)"),
    (77,  "Kyle Pitts Sr. (ATL)"),
    (78,  "KC Concepcion (CLE)"),
    (79,  "Javonte Williams (DAL)"),
    (80,  "Sam Darnold (SEA)"),
    (81,  "Cam Skattebo (NYG)"),
    (82,  "Jadarian Price (SEA)"),
    (83,  "Josh Jacobs (GB)"),
    (84,  "Malik Willis (MIA)"),
    (85,  "Kenyon Sadiq (NYJ)"),
    (86,  "Alec Pierce (IND)"),
    (87,  "Jordan Addison (MIN)"),
    (88,  "Christian Watson (GB)"),
    (89,  "DJ Moore (BUF)"),
    (90,  "Daniel Jones (IND)"),
    (91,  "Terry McLaurin (WAS)"),
    (92,  "DK Metcalf (PIT)"),
    (93,  "Bryce Young (CAR)"),
    (94,  "Derrick Henry (BAL)"),
    (95,  "Eli Stowers (PHI)"),
    (96,  "Omar Cooper Jr. (NYJ)"),
    (97,  "Michael Wilson (ARI)"),
    (98,  "Bhayshul Tuten (JAC)"),
    (99,  "Ricky Pearsall (SF)"),
    (100, "Ty Simpson (LAR)"),
    (101, "Oronde Gadsden II (LAC)"),
    (102, "Xavier Worthy (KC)"),
    (103, "D'Andre Swift (CHI)"),
    (104, "Matthew Stafford (LAR)"),
    (105, "Denzel Boston (CLE)"),
    (106, "Courtland Sutton (DEN)"),
    (107, "Davante Adams (LAR)"),
    (108, "Jake Ferguson (DAL)"),
    (109, "Wan'Dale Robinson (TEN)"),
    (110, "Jayden Higgins (HOU)"),
    (111, "RJ Harvey (DEN)"),
    (112, "Dalton Kincaid (BUF)"),
    (113, "Isaiah Likely (NYG)"),
    (114, "Mike Evans (SF)"),
    (115, "Michael Pittman Jr. (PIT)"),
    (116, "Jakobi Meyers (JAC)"),
    (117, "Parker Washington (JAC)"),
    (118, "George Kittle (SF)"),
    (119, "Josh Downs (IND)"),
    (120, "David Montgomery (HOU)"),
    (121, "Matthew Golden (GB)"),
    (122, "Jayden Reed (GB)"),
    (123, "Kyle Monangai (CHI)"),
    (124, "Chris Godwin Jr. (TB)"),
    (125, "Quentin Johnston (LAC)"),
    (126, "Zach Charbonnet (SEA)"),
    (127, "Jaylen Warren (PIT)"),
    (128, "Brenton Strange (JAC)"),
    (129, "Travis Hunter (JAC)"),
    (130, "Khalil Shakir (BUF)"),
    (131, "Romeo Doubs (NE)"),
    (132, "Michael Penix Jr. (ATL)"),
    (133, "Chuba Hubbard (CAR)"),
    (134, "Blake Corum (LAR)"),
    (135, "Jonah Coleman (DEN)"),
    (136, "Antonio Williams (WAS)"),
    (137, "Rhamondre Stevenson (NE)"),
    (138, "Rico Dowdle (PIT)"),
    (139, "Chris Bell (MIA)"),
    (140, "Brandon Aiyuk (SF)"),
    (141, "Germie Bernard (PIT)"),
    (142, "Jalen Coker (CAR)"),
    (143, "J.J. McCarthy (MIN)"),
    (144, "Tony Pollard (TEN)"),
    (145, "Jauan Jennings (MIN)"),
    (146, "Dallas Goedert (PHI)"),
    (147, "Mark Andrews (BAL)"),
    (148, "Chig Okonkwo (WAS)"),
    (149, "Rashid Shaheed (SEA)"),
    (150, "Kenneth Gainwell (TB)"),
    (151, "Terrance Ferguson (LAR)"),
    (152, "AJ Barner (SEA)"),
    (153, "Tre' Harris (LAC)"),
    (154, "Jalen McMillan (TB)"),
    (155, "Woody Marks (HOU)"),
    (156, "Jacory Croskey-Merritt (WAS)"),
    (157, "De'Zhaun Stribling (SF)"),
    (158, "Tyler Allgeier (ARI)"),
    (159, "J.K. Dobbins (DEN)"),
    (160, "Tyrone Tracy Jr. (NYG)"),
    (161, "Jonathon Brooks (CAR)"),
    (162, "Ted Hurst III (TB)"),
    (163, "Jaylin Noel (HOU)"),
    (164, "Elijah Sarratt (BAL)"),
    (165, "Chris Brazzell II (CAR)"),
    (166, "T.J. Hockenson (MIN)"),
    (167, "Travis Kelce (KC)"),
    (168, "Juwan Johnson (NO)"),
    (169, "Nicholas Singleton (TEN)"),
    (170, "Rachaad White (WAS)"),
    (171, "Malachi Fields (NYG)"),
    (172, "Jordan Mason (MIN)"),
    (173, "Emmett Johnson (KC)"),
    (174, "Jerry Jeudy (CLE)"),
    (175, "Max Klare (LAR)"),
    (176, "Oscar Delp (NO)"),
    (177, "Zachariah Branch (ATL)"),
    (178, "Chris Rodriguez Jr. (JAC)"),
    (179, "Skyler Bell (BUF)"),
    (180, "Hunter Henry (NE)"),
    (181, "Tyjae Spears (TEN)"),
    (182, "Dylan Sampson (CLE)"),
    (183, "Pat Bryant (DEN)"),
    (184, "Mike Washington Jr. (LV)"),
    (185, "Stefon Diggs (FA)"),
    (186, "Mason Taylor (NYJ)"),
    (187, "Tua Tagovailoa (ATL)"),
    (188, "Ja'Kobi Lane (BAL)"),
    (189, "Troy Franklin (DEN)"),
    (190, "Kaytron Allen (WAS)"),
    (191, "Dalton Schultz (HOU)"),
    (192, "Gunnar Helm (TEN)"),
    (193, "Deebo Samuel Sr. (FA)"),
    (194, "Aaron Jones Sr. (MIN)"),
    (195, "Adonai Mitchell (NYJ)"),
    (196, "Kayshon Boutte (NE)"),
    (197, "Isiah Pacheco (DET)"),
    (198, "David Njoku (LAC)"),
    (199, "Cade Otton (TB)"),
    (200, "Isaac TeSlaa (DET)"),
]

# Known mismatches: FantasyPros name (after stripping team/suffix) → canonical master name
NAME_MAP = {
    "Chig Okonkwo": "Chigoziem Okonkwo",
}


def strip_team(name):
    """Remove trailing (TEAM) from player name."""
    return re.sub(r'\s*\([A-Z]+\)\s*$', '', name).strip()


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
    for rank, raw in RAW:
        clean = strip_team(raw)
        canonical = NAME_MAP.get(clean, clean)
        rankings.append((rank, canonical))

    with open(MASTER_PATH, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    header = rows[0]
    data = rows[1:]

    fp_idx = header.index(OLD_COL)
    header[fp_idx] = NEW_COL

    name_to_idx = {normalize(row[0]): i for i, row in enumerate(data)}

    for row in data:
        row[fp_idx] = ""

    matched = 0
    unmatched = []

    for rank, name in rankings:
        norm = normalize(name)
        if norm in name_to_idx:
            data[name_to_idx[norm]][fp_idx] = str(rank)
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
        new_row[fp_idx] = str(rank)
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
