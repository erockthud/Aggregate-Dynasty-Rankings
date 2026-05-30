#!/usr/bin/env python3
"""Update HarryKnowsBall baseball rankings from Mar 2026 to May 2026."""

import csv
import re
import unicodedata
import subprocess

MASTER_PATH = "baseball/baseball_rankings_master.csv"
OLD_COL = "HarryKnowsBall (Crowdsourced, 2026-03-03)"
NEW_COL = "HarryKnowsBall (Crowdsourced, 2026-05-29)"

# Draft pick slots to skip (not real players)
SKIP = {
    "2027 Early 1st", "2028 Early 1st", "2027 Mid 1st", "2028 Mid 1st",
    "2027 Late 1st", "2028 Late 1st", "2027 Early 2nd",
}

NEW_RANKINGS = [
    (1,   "Shohei Ohtani"),
    (2,   "Bobby Witt Jr."),
    (3,   "Paul Skenes"),
    (4,   "Juan Soto"),
    (5,   "Elly De La Cruz"),
    (6,   "Junior Caminero"),
    (7,   "Corbin Carroll"),
    (8,   "Nick Kurtz"),
    (9,   "Konnor Griffin"),
    (10,  "Aaron Judge"),
    (11,  "James Wood"),
    (12,  "Ronald Acuna Jr."),
    (13,  "Tarik Skubal"),
    (14,  "Julio Rodriguez"),
    (15,  "Gunnar Henderson"),
    (16,  "Jacob Misiorowski"),
    (17,  "Yordan Alvarez"),
    (18,  "Vladimir Guerrero Jr."),
    (19,  "Kevin McGonigle"),
    (20,  "Jackson Chourio"),
    (21,  "Roman Anthony"),
    (22,  "Yoshinobu Yamamoto"),
    (23,  "Cam Schlittler"),
    (24,  "Garrett Crochet"),
    (25,  "Chase Burns"),
    (26,  "JJ Wetherholt"),
    (27,  "Fernando Tatis Jr."),
    (28,  "Ben Rice"),
    (29,  "Bryan Woo"),
    (30,  "Sal Stewart"),
    (31,  "Nolan McLean"),
    (32,  "Jose Ramirez"),
    (33,  "Cristopher Sanchez"),
    (34,  "Hunter Brown"),
    (35,  "Drake Baldwin"),
    (36,  "Kyle Tucker"),
    (37,  "CJ Abrams"),
    (38,  "Wyatt Langford"),
    (39,  "Zach Neto"),
    (40,  "Jesus Made"),
    (41,  "Leo De Vries"),
    (42,  "Brice Turang"),
    (43,  "Mason Miller"),
    (44,  "Jackson Merrill"),
    (45,  "Riley Greene"),
    (46,  "Hunter Greene"),
    (47,  "Trey Yesavage"),
    (48,  "Samuel Basallo"),
    (49,  "Logan Gilbert"),
    (50,  "Cal Raleigh"),
    (51,  "Shea Langeliers"),
    (52,  "Matt Olson"),
    (53,  "Pete Crow-Armstrong"),
    (54,  "Kyle Schwarber"),
    (55,  "George Kirby"),
    (56,  "Max Fried"),
    (57,  "Eury Perez"),
    (58,  "Jazz Chisholm Jr."),
    (59,  "Kade Anderson"),
    (60,  "Ketel Marte"),
    (61,  "Tyler Soderstrom"),
    (62,  "Joe Ryan"),
    (63,  "Oneil Cruz"),
    (64,  "Chase DeLauter"),
    (65,  "Munetaka Murakami"),
    (66,  "Maikel Garcia"),
    (67,  "Francisco Lindor"),
    (68,  "Bryce Harper"),
    (69,  "Logan Webb"),
    (70,  "William Contreras"),
    (71,  "Jac Caglianone"),
    (72,  "Cole Ragans"),
    (73,  "Austin Riley"),
    (74,  "Max Clark"),
    (75,  "Carter Jensen"),
    (76,  "Rafael Devers"),
    (77,  "Freddy Peralta"),
    (78,  "Jordan Walker"),
    (79,  "Seth Hernandez"),
    (80,  "Pete Alonso"),
    (81,  "Payton Tolle"),
    (82,  "Travis Bazzana"),
    (83,  "Bubba Chandler"),
    (84,  "Gavin Williams"),
    (85,  "Colt Emerson"),
    (86,  "Spencer Schwellenbach"),
    (87,  "Dylan Cease"),
    (88,  "Sebastian Walcott"),
    (89,  "Geraldo Perdomo"),
    (90,  "Walker Jenkins"),
    (91,  "Jackson Holliday"),
    (92,  "Mookie Betts"),
    (93,  "Bo Bichette"),
    (94,  "Jesus Luzardo"),
    (95,  "Nico Hoerner"),
    (96,  "Andy Pages"),
    (97,  "Michael Harris II"),
    (98,  "Bryce Eldridge"),
    (99,  "Trea Turner"),
    (100, "Connelly Early"),
    (101, "Corey Seager"),
    (102, "Spencer Strider"),
    (103, "Colson Montgomery"),
    (104, "Thomas White"),
    (105, "Vinnie Pasquantino"),
    (106, "Luis Pena"),
    (107, "Cody Bellinger"),
    (108, "Parker Messick"),
    (109, "Josue De Paula"),
    (110, "Jacob Wilson"),
    (111, "Carson Benge"),
    (112, "Noah Schultz"),
    (113, "MacKenzie Gore"),
    (114, "Jared Jones"),
    (115, "Jarren Duran"),
    (116, "Eli Willits"),
    (117, "Brent Rooker"),
    (118, "Josh Naylor"),
    (119, "Edward Florentino"),
    (120, "Kyle Harrison"),
    (121, "Jose Soriano"),
    (122, "Robby Snelling"),
    (123, "Luke Keaschall"),
    (124, "Ivan Herrera"),
    (125, "Hunter Goodman"),
    (126, "Sandy Alcantara"),
    (127, "Adley Rutschman"),
    # 128: 2027 Early 1st — skipped
    (129, "Andrew Painter"),
    (130, "Chris Sale"),
    (131, "Wilyer Abreu"),
    (132, "Michael King"),
    (133, "Aidan Miller"),
    (134, "Cade Horton"),
    (135, "Emmet Sheehan"),
    (136, "Nick Lodolo"),
    (137, "Byron Buxton"),
    (138, "Shane McClanahan"),
    # 139: 2028 Early 1st — skipped
    (140, "Edward Cabrera"),
    (141, "Manny Machado"),
    (142, "Jhoan Duran"),
    (143, "Jeremy Pena"),
    (144, "Cam Smith"),
    (145, "Framber Valdez"),
    (146, "Dylan Crews"),
    (147, "Tyler Glasnow"),
    (148, "Michael Busch"),
    (149, "Ryan Waldschmidt"),
    (150, "Seiya Suzuki"),
    (151, "Lawrence Butler"),
    (152, "Rainiel Rodriguez"),
    (153, "Jonah Tong"),
    (154, "Zack Wheeler"),
    (155, "Moises Ballesteros"),
    (156, "Kyle Stowers"),
    (157, "Braxton Ashcraft"),
    (158, "Alex Bregman"),
    (159, "Ryan Sloan"),
    (160, "Braden Montgomery"),
    (161, "Marcelo Mayer"),
    (162, "Jonathan Aranda"),
    (163, "Mike Trout"),
    (164, "Kris Bubic"),
    (165, "Zyhir Hope"),
    (166, "Blake Snell"),
    (167, "Corbin Burnes"),
    (168, "Jo Adell"),
    (169, "Jordan Lawlar"),
    (170, "Charlie Condon"),
    (171, "Agustin Ramirez"),
    (172, "Will Smith"),
    (173, "Ethan Holliday"),
    (174, "Kyle Bradish"),
    (175, "Xavier Edwards"),
    (176, "Joshua Baez"),
    (177, "Logan Henderson"),
    (178, "Jasson Dominguez"),
    (179, "A.J. Ewing"),
    (180, "Jordan Westburg"),
    (181, "Cade Smith"),
    (182, "Ozzie Albies"),
    (183, "Jacob deGrom"),
    (184, "Kazuma Okamoto"),
    (185, "George Lombard Jr."),
    (186, "Dalton Rushing"),
    (187, "Andres Munoz"),
    (188, "Bryce Rainer"),
    (189, "Randy Arozarena"),
    (190, "Taj Bradley"),
    (191, "Caleb Bonemer"),
    (192, "Ryan Weathers"),
    (193, "Shota Imanaga"),
    (194, "Roki Sasaki"),
    (195, "Franklin Arias"),
    (196, "Daylen Lile"),
    (197, "Freddie Freeman"),
    (198, "Eduardo Quintero"),
    (199, "Will Warren"),
    (200, "Emerson Hancock"),
    # 201: 2027 Mid 1st — skipped
    (202, "Jackson Jobe"),
    (203, "Ranger Suarez"),
    (204, "Cole Young"),
    (205, "Owen Caissie"),
    (206, "JoJo Parker"),
    (207, "Justin Crawford"),
    (208, "Max Meyer"),
    (209, "Chandler Simpson"),
    (210, "Kyle Teel"),
    (211, "Bryce Miller"),
    (212, "Miguel Vargas"),
    (213, "Drew Rasmussen"),
    (214, "Emmanuel Rodriguez"),
    (215, "Spencer Torkelson"),
    (216, "Matt McLain"),
    (217, "Ceddanne Rafaela"),
    (218, "Jamie Arnold"),
    (219, "Otto Lopez"),
    (220, "Steven Kwan"),
    (221, "Didier Fuentes"),
    (222, "Edwin Diaz"),
    (223, "Dylan Beavers"),
    (224, "Jack Leiter"),
    (225, "Matt Shaw"),
    (226, "Shane Baz"),
    (227, "Carlos Lagrange"),
    (228, "Spencer Arrighetti"),
    # 229: 2028 Mid 1st — skipped
    (230, "Sam Antonacci"),
    (231, "Liam Doyle"),
    (232, "Tatsuya Imai"),
    (233, "Brandon Lowe"),
    (234, "Kaelen Culpepper"),
    (235, "Cam Caminiti"),
    (236, "Josh Hader"),
    (237, "Gerrit Cole"),
    (238, "Luis Robert Jr."),
    (239, "Andrew Abbott"),
    (240, "Brendan Donovan"),
    (241, "Tanner Bibee"),
    (242, "Trevor Rogers"),
    (243, "Mike Sirota"),
    (244, "Chase Dollander"),
    (245, "Kevin Gausman"),
    (246, "Gage Jump"),
    (247, "Lazaro Montes"),
    (248, "Francisco Alvarez"),
    (249, "Ryan Pepiot"),
    (250, "Josuar Gonzalez"),
    (251, "Alec Burleson"),
    (252, "Ralphy Velazquez"),
    (253, "Dillon Dingler"),
    (254, "J.R. Ritchie"),
    (255, "Luis Hernandez"),
    (256, "Colt Keith"),
    (257, "Mick Abel"),
    (258, "Jakob Marsee"),
    (259, "Casey Mize"),
    # 260: 2027 Late 1st — skipped
    (261, "Hagen Smith"),
    (262, "Jett Williams"),
    (263, "Dax Kilby"),
    (264, "Emil Morales"),
    (265, "Andrew Fischer"),
    (266, "James Tibbs III"),
    (267, "Gage Wood"),
    (268, "Ian Happ"),
    (269, "Rhett Lowder"),
    (270, "Noelvi Marte"),
    (271, "Willson Contreras"),
    (272, "Kendry Chourio"),
    (273, "Landen Roupp"),
    (274, "Abner Uribe"),
    (275, "Spencer Jones"),
    (276, "Willy Adames"),
    (277, "Grant Taylor"),
    (278, "Travis Sykora"),
    (279, "Heliot Ramos"),
    (280, "Alfredo Duno"),
    (281, "Christian Yelich"),
    (282, "Isaac Paredes"),
    (283, "Hurston Waldrep"),
    (284, "Addison Barger"),
    (285, "Liam Hicks"),
    (286, "Tyler Bremner"),
    (287, "Josue Briceno"),
    (288, "Theo Gillen"),
    (289, "Pablo Lopez"),
    (290, "Aiva Arquette"),
    (291, "Mickey Moniak"),
    (292, "Reid Detmers"),
    (293, "Carlos Rodon"),
    (294, "Elmer Rodriguez-Cruz"),
    (295, "Brandon Woodruff"),
    (296, "Troy Melton"),
    (297, "Daniel Palencia"),
    # 298: 2028 Late 1st — skipped
    (299, "Noah Cameron"),
    (300, "Ethan Conrad"),
    (301, "Michael Arroyo"),
    (302, "Zebby Matthews"),
    (303, "Bryce Elder"),
    (304, "Kyle Manzardo"),
    (305, "Evan Carter"),
    (306, "Arjun Nimmala"),
    (307, "Daulton Varsho"),
    (308, "Ethan Salas"),
    (309, "Joey Cantillo"),
    (310, "Cade Cavalli"),
    (311, "Coby Mayo"),
    (312, "Jarlin Susana"),
    (313, "Esmerlyn Valdez"),
    (314, "Justin Wrobleski"),
    (315, "Brandon Sproat"),
    (316, "Kyson Witherspoon"),
    (317, "Quinn Priester"),
    (318, "Masyn Winn"),
    (319, "Yandy Diaz"),
    (320, "Taylor Ward"),
    (321, "Kerry Carpenter"),
    (322, "Ezequiel Tovar"),
    (323, "Shane Bieber"),
    (324, "Dansby Swanson"),
    (325, "Kristian Campbell"),
    (326, "Nick Pivetta"),
    (327, "AJ Smith-Shawver"),
    (328, "Max Muncy"),
    (329, "Devin Williams"),
    (330, "Jhonny Level"),
    (331, "Bryan Reynolds"),
    (332, "Anthony Eyanson"),
    (333, "Brady House"),
    (334, "Zac Gallen"),
    (335, "Caden Scarborough"),
    (336, "Josh Jung"),
    (337, "Carson Williams"),
    (338, "Royce Lewis"),
    (339, "Eugenio Suarez"),
    (340, "Henry Bolte"),
    (341, "Jaison Chourio"),
    (342, "Justin Steele"),
    (343, "Nathan Eovaldi"),
    (344, "Braylon Payne"),
    (345, "Robbie Ray"),
    (346, "Anthony Volpe"),
    (347, "Andrew Vaughn"),
    (348, "Teoscar Hernandez"),
    (349, "Sal Frelick"),
    (350, "Christian Scott"),
    (351, "Kevin Alcantara"),
    (352, "Grayson Rodriguez"),
    (353, "Spencer Steer"),
    (354, "Angel Martinez"),
    (355, "Edwin Arroyo"),
    (356, "Joe Mack"),
    (357, "Jose Altuve"),
    (358, "Christian Moore"),
    (359, "Tanner McDougal"),
    (360, "Steele Hall"),
    (361, "Luis Garcia Jr."),
    (362, "Kruz Schoolcraft"),
    (363, "Jaxon Wiggins"),
    (364, "Brandon Nimmo"),
    (365, "Colton Cowser"),
    (366, "Jonny Farmelo"),
    (367, "David Bednar"),
    (368, "Johnny King"),
    (369, "Garrett Mitchell"),
    (370, "Ryan Helsley"),
    (371, "Matthew Liberatore"),
    (372, "Ryne Nelson"),
    (373, "Nolan Schanuel"),
    (374, "Cooper Pratt"),
    (375, "River Ryan"),
    (376, "Mitch Keller"),
    (377, "Xavier Isaac"),
    # 378: 2027 Early 2nd — skipped
    (379, "Ben Brown"),
    (380, "Matt Chapman"),
    (381, "Cam Collier"),
    (382, "Brayan Bello"),
    (383, "Sonny Gray"),
    (384, "Felnin Celesten"),
    (385, "Gabriel Moreno"),
    (386, "Gleyber Torres"),
    (387, "Xavier Neyens"),
    (388, "Jung Hoo Lee"),
    (389, "Caleb Durbin"),
    (390, "Jacob Reimer"),
    (391, "Luis Castillo"),
    (392, "Alejandro Kirk"),
    (393, "Yainer Diaz"),
    (394, "Aroldis Chapman"),
    (395, "Nate George"),
    (396, "Bryson Stott"),
    (397, "Ryan Clifford"),
    (398, "Michael Soroka"),
    (399, "Mark Vientos"),
    (400, "Brody Hopkins"),
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
    with open(MASTER_PATH, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    header = rows[0]
    data = rows[1:]

    # Rename column
    hkb_idx = header.index(OLD_COL)
    header[hkb_idx] = NEW_COL

    # Build lookup: normalized name -> row index
    name_to_idx = {}
    for i, row in enumerate(data):
        norm = normalize(row[0])
        name_to_idx[norm] = i

    # Clear all existing HKB rankings
    for row in data:
        row[hkb_idx] = ""

    matched = 0
    unmatched = []

    for rank, name in NEW_RANKINGS:
        norm = normalize(name)
        if norm in name_to_idx:
            data[name_to_idx[norm]][hkb_idx] = str(rank)
            matched += 1
        else:
            unmatched.append((rank, name))

    print(f"Matched: {matched}")
    print(f"New players to add: {len(unmatched)}")
    for rank, name in unmatched:
        print(f"  [{rank}] {name}")

    # Add new rows for unmatched players
    for rank, name in unmatched:
        new_row = [""] * len(header)
        new_row[0] = name
        new_row[hkb_idx] = str(rank)
        data.append(new_row)

    with open(MASTER_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)

    print(f"\nWrote {len(data)} rows to {MASTER_PATH}")

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
