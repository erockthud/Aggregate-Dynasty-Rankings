#!/usr/bin/env python3
"""Update Baseball America dynasty rankings from Feb 2026 to May 2026."""

import csv
import re
import unicodedata
import subprocess

MASTER_PATH = "baseball/baseball_rankings_master.csv"
OLD_COL = "Baseball America (Feb 2026)"
NEW_COL = "Baseball America (Apr 2026)"

NEW_RANKINGS = [
    (1,   "Shohei Ohtani"),
    (2,   "Juan Soto"),
    (3,   "Bobby Witt Jr."),
    (4,   "Tarik Skubal"),
    (5,   "Paul Skenes"),
    (6,   "Elly De La Cruz"),
    (7,   "Gunnar Henderson"),
    (8,   "Corbin Carroll"),
    (9,   "Julio Rodriguez"),
    (10,  "Aaron Judge"),
    (11,  "Junior Caminero"),
    (12,  "Jackson Chourio"),
    (13,  "Fernando Tatis Jr."),
    (14,  "Vladimir Guerrero Jr."),
    (15,  "Nick Kurtz"),
    (16,  "Jose Ramirez"),
    (17,  "Ronald Acuna Jr."),
    (18,  "Yordan Alvarez"),
    (19,  "Roman Anthony"),
    (20,  "James Wood"),
    (21,  "Konnor Griffin"),
    (22,  "Kevin McGonigle"),
    (23,  "Wyatt Langford"),
    (24,  "Garrett Crochet"),
    (25,  "Kyle Tucker"),
    (26,  "Jazz Chisholm Jr."),
    (27,  "Yoshinobu Yamamoto"),
    (28,  "Zach Neto"),
    (29,  "Logan Gilbert"),
    (30,  "CJ Abrams"),
    (31,  "Jackson Merrill"),
    (32,  "Manny Machado"),
    (33,  "Bryce Harper"),
    (34,  "Francisco Lindor"),
    (35,  "JJ Wetherholt"),
    (36,  "Pete Alonso"),
    (37,  "Ketel Marte"),
    (38,  "Cal Raleigh"),
    (39,  "Hunter Brown"),
    (40,  "Nolan McLean"),
    (41,  "Trea Turner"),
    (42,  "Oneil Cruz"),
    (43,  "Mookie Betts"),
    (44,  "Cristopher Sanchez"),
    (45,  "Joe Ryan"),
    (46,  "Eury Perez"),
    (47,  "Rafael Devers"),
    (48,  "Kyle Schwarber"),
    (49,  "Jesus Made"),
    (50,  "Corey Seager"),
    (51,  "Ben Rice"),
    (52,  "Colt Emerson"),
    (53,  "Matt Olson"),
    (54,  "Riley Greene"),
    (55,  "Walker Jenkins"),
    (56,  "Chris Sale"),
    (57,  "Jacob deGrom"),
    (58,  "George Kirby"),
    (59,  "Logan Webb"),
    (60,  "Samuel Basallo"),
    (61,  "Bryan Woo"),
    (62,  "Chase Burns"),
    (63,  "Jacob Misiorowski"),
    (64,  "Max Clark"),
    (65,  "Mason Miller"),
    (66,  "Freddie Freeman"),
    (67,  "William Contreras"),
    (68,  "Sal Stewart"),
    (69,  "Brice Turang"),
    (70,  "Cam Schlittler"),
    (71,  "Leo De Vries"),
    (72,  "Jackson Holliday"),
    (73,  "Jeremy Pena"),
    (74,  "Austin Riley"),
    (75,  "Freddy Peralta"),
    (76,  "Luke Keaschall"),
    (77,  "Cody Bellinger"),
    (78,  "Randy Arozarena"),
    (79,  "Brent Rooker"),
    (80,  "Andy Pages"),
    (81,  "Shea Langeliers"),
    (82,  "Vinnie Pasquantino"),
    (83,  "Chase DeLauter"),
    (84,  "Carson Benge"),
    (85,  "Caleb Bonemer"),
    (86,  "Pete Crow-Armstrong"),
    (87,  "Trey Yesavage"),
    (88,  "Josue De Paula"),
    (89,  "Luis Pena"),
    (90,  "Josh Naylor"),
    (91,  "Agustin Ramirez"),
    (92,  "Max Fried"),
    (93,  "Tyler Soderstrom"),
    (94,  "Jose Altuve"),
    (95,  "Drake Baldwin"),
    (96,  "Cole Ragans"),
    (97,  "Aidan Miller"),
    (98,  "Geraldo Perdomo"),
    (99,  "Hunter Greene"),
    (100, "Lawrence Butler"),
    (101, "Dylan Cease"),
    (102, "Jarren Duran"),
    (103, "Michael Harris II"),
    (104, "Bo Bichette"),
    (105, "Michael Busch"),
    (106, "Rainiel Rodriguez"),
    (107, "Bryce Eldridge"),
    (108, "Kyle Bradish"),
    (109, "Jesus Luzardo"),
    (110, "Jordan Westburg"),
    (111, "Andres Munoz"),
    (112, "Christian Yelich"),
    (113, "Tyler Glasnow"),
    (114, "Gerrit Cole"),
    (115, "Michael King"),
    (116, "MacKenzie Gore"),
    (117, "Blake Snell"),
    (118, "Spencer Strider"),
    (119, "Nick Lodolo"),
    (120, "Cam Smith"),
    (121, "Edward Florentino"),
    (122, "Framber Valdez"),
    (123, "Kevin Gausman"),
    (124, "Jhoan Duran"),
    (125, "Maikel Garcia"),
    (126, "Willy Adames"),
    (127, "Alex Bregman"),
    (128, "Payton Tolle"),
    (129, "Byron Buxton"),
    (130, "Royce Lewis"),
    (131, "Jacob Wilson"),
    (132, "Ozzie Albies"),
    (133, "Eduardo Quintero"),
    (134, "Will Smith"),
    (135, "Kyle Manzardo"),
    (136, "Jo Adell"),
    (137, "Mike Trout"),
    (138, "Ivan Herrera"),
    (139, "Shane McClanahan"),
    (140, "Cade Smith"),
    (141, "Steven Kwan"),
    (142, "Addison Barger"),
    (143, "Luis Robert Jr."),
    (144, "Nico Hoerner"),
    (145, "Francisco Alvarez"),
    (146, "Emmet Sheehan"),
    (147, "Teoscar Hernandez"),
    (148, "Seiya Suzuki"),
    (149, "Jose Soriano"),
    (150, "Sebastian Walcott"),
    (151, "Connelly Early"),
    (152, "Bubba Chandler"),
    (153, "Carter Jensen"),
    (154, "Andrew Painter"),
    (155, "Munetaka Murakami"),
    (156, "Thomas White"),
    (157, "Spencer Schwellenbach"),
    (158, "Jac Caglianone"),
    (159, "Zack Wheeler"),
    (160, "Kyle Stowers"),
    (161, "Yandy Diaz"),
    (162, "Carlos Rodon"),
    (163, "Joshua Baez"),
    (164, "Ryan Waldschmidt"),
    (165, "Seth Hernandez"),
    (166, "Travis Bazzana"),
    (167, "Zyhir Hope"),
    (168, "Jonah Tong"),
    (169, "Mike Sirota"),
    (170, "Josuar Gonzalez"),
    (171, "Owen Caissie"),
    (172, "Nathan Eovaldi"),
    (173, "Shota Imanaga"),
    (174, "Isaac Paredes"),
    (175, "Edwin Diaz"),
    (176, "Gavin Williams"),
    (177, "Ranger Suarez"),
    (178, "Tanner Bibee"),
    (179, "Matt McLain"),
    (180, "Jordan Lawlar"),
    (181, "Ian Happ"),
    (182, "Anthony Volpe"),
    (183, "Brandon Nimmo"),
    (184, "Mark Vientos"),
    (185, "Eugenio Suarez"),
    (186, "Shane Baz"),
    (187, "Luis Castillo"),
    (188, "Hunter Goodman"),
    (189, "George Springer"),
    (190, "Shane Bieber"),
    (191, "Edward Cabrera"),
    (192, "Jack Flaherty"),
    (193, "Sonny Gray"),
    (194, "Matt Chapman"),
    (195, "Gleyber Torres"),
    (196, "Brett Baty"),
    (197, "Jonathan Aranda"),
    (198, "Robbie Ray"),
    (199, "Grayson Rodriguez"),
    (200, "Sandy Alcantara"),
    (201, "Matt Shaw"),
    (202, "Kade Anderson"),
    (203, "Noah Schultz"),
    (204, "Ralphy Velazquez"),
    (205, "Braden Montgomery"),
    (206, "Robby Snelling"),
    (207, "Tatsuya Imai"),
    (208, "Brandon Woodruff"),
    (209, "Dylan Crews"),
    (210, "Jared Jones"),
    (211, "Corbin Burnes"),
    (212, "Wilyer Abreu"),
    (213, "Bryce Miller"),
    (214, "Justin Steele"),
    (215, "Ryan Sloan"),
    (216, "Jhonny Level"),
    (217, "Franklin Arias"),
    (218, "Parker Messick"),
    (219, "Emmanuel Rodriguez"),
    (220, "Kaelen Culpepper"),
    (221, "JoJo Parker"),
    (222, "Kazuma Okamoto"),
    (223, "Brandon Lowe"),
    (224, "Masyn Winn"),
    (225, "Adley Rutschman"),
    (226, "Kyle Teel"),
    (227, "Spencer Torkelson"),
    (228, "Ceddanne Rafaela"),
    (229, "Otto Lopez"),
    (230, "Drew Rasmussen"),
    (231, "Jeff Hoffman"),
    (232, "Aaron Nola"),
    (233, "Devin Williams"),
    (234, "Dalton Rushing"),
    (235, "Kris Bubic"),
    (236, "Ezequiel Tovar"),
    (237, "Taj Bradley"),
    (238, "Zac Gallen"),
    (239, "Alec Burleson"),
    (240, "Willson Contreras"),
    (241, "Josh Hader"),
    (242, "Moises Ballesteros"),
    (243, "Xavier Edwards"),
    (244, "Kerry Carpenter"),
    (245, "Heliot Ramos"),
    (246, "Colton Cowser"),
    (247, "Daylen Lile"),
    (248, "Bryson Stott"),
    (249, "Alejandro Kirk"),
    (250, "Trevor Story"),
    (251, "Brendan Donovan"),
    (252, "Austin Wells"),
    (253, "Yainer Diaz"),
    (254, "Dylan Beavers"),
    (255, "Jordan Walker"),
    (256, "Gabriel Moreno"),
    (257, "Joe Musgrove"),
    (258, "Ryan Pepiot"),
    (259, "Alec Bohm"),
    (260, "Bryan Reynolds"),
    (261, "Xander Bogaerts"),
    (262, "Dansby Swanson"),
    (263, "Marcelo Mayer"),
    (264, "Jack Leiter"),
    (265, "Ryan Weathers"),
    (266, "Matthew Boyd"),
    (267, "Ryne Nelson"),
    (268, "Zebby Matthews"),
    (269, "Andrew Abbott"),
    (270, "Taylor Ward"),
    (271, "Quinn Priester"),
    (272, "Trevor Rogers"),
    (273, "Casey Mize"),
    (274, "Carlos Correa"),
    (275, "Sal Frelick"),
    (276, "Caleb Durbin"),
    (277, "Colt Keith"),
    (278, "Luis Garcia Jr."),
    (279, "Coby Mayo"),
    (280, "Triston Casas"),
    (281, "Chandler Simpson"),
    (282, "Matt Wallner"),
    (283, "Dax Kilby"),
    (284, "Daulton Varsho"),
    (285, "Carlos Lagrange"),
    (286, "Grant Taylor"),
    (287, "A.J. Ewing"),
    (288, "Eli Willits"),
    (289, "Brenton Doyle"),
    (290, "AJ Smith-Shawver"),
    (291, "David Bednar"),
    (292, "Will Warren"),
    (293, "Brayan Bello"),
    (294, "Josue Briceno"),
    (295, "Ryan Helsley"),
    (296, "Ryan Clifford"),
    (297, "Pete Fairbanks"),
    (298, "George Lombard Jr."),
    (299, "Ronny Cruz"),
    (300, "Theo Gillen"),
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
    # Build new rankings lookup: normalized_name -> rank
    new_lookup = {}
    for rank, name in NEW_RANKINGS:
        key = normalize(name)
        new_lookup[key] = rank

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

    # Clear the column for all existing rows (dropped players get blanked)
    for row in rows:
        row[NEW_COL] = ""

    # Track matched keys
    matched_keys = set()

    # Update existing rows
    for row in rows:
        key = normalize(row["Player"])
        if key in new_lookup:
            row[NEW_COL] = new_lookup[key]
            matched_keys.add(key)

    # Find unmatched new players
    unmatched = []
    for rank, name in NEW_RANKINGS:
        key = normalize(name)
        if key not in matched_keys:
            unmatched.append((rank, name))

    print(f"Matched: {len(matched_keys)} players")
    print(f"New players to add: {len(unmatched)}")
    for rank, name in unmatched:
        print(f"  [{rank}] {name}")

    # Add new rows for unmatched players
    for rank, name in unmatched:
        new_row = {fn: "" for fn in fieldnames}
        new_row["Player"] = name
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
