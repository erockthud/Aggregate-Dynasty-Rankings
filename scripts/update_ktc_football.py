#!/usr/bin/env python3
"""Update KeepTradeCut football rankings from Mar 2026 to May 2026."""

import csv
import re
import unicodedata
import subprocess

MASTER_PATH = "football/football_rankings_master.csv"
OLD_COL = "KeepTradeCut (Crowdsourced, 2026-03)"
NEW_COL = "KeepTradeCut (Crowdsourced, 2026-05)"

# Raw data: rank, raw_name (with team code appended)
# PICK entries are omitted; their rank numbers are preserved in the numbering.
RAW = [
    (1,   "Bijan RobinsonATL"),
    (2,   "Josh AllenBUF"),
    (3,   "Ja'Marr ChaseCIN"),
    (4,   "Jaxon Smith-NjigbaSEA"),
    (5,   "Jahmyr GibbsDET"),
    (6,   "Drake MayeNEP"),
    (7,   "Puka NacuaLAR"),
    (8,   "Brock BowersLVR"),
    (9,   "Caleb WilliamsCHI"),
    (10,  "Jayden DanielsWAS"),
    (11,  "Amon-Ra St. BrownDET"),
    (12,  "Justin JeffersonMIN"),
    (13,  "Lamar JacksonBAL"),
    (14,  "Malik NabersNYG"),
    (15,  "Jeremiyah LoveRARI"),
    (16,  "Ashton JeantyLVR"),
    (17,  "Trey McBrideARI"),
    (18,  "Joe BurrowCIN"),
    (19,  "CeeDee LambDAL"),
    # 20: 2027 Early 1st — skipped
    (21,  "De'Von AchaneMIA"),
    (22,  "Drake LondonATL"),
    (23,  "Justin HerbertLAC"),
    (24,  "Omarion HamptonLAC"),
    (25,  "Patrick MahomesKCC"),
    (26,  "Jaxson DartNYG"),
    (27,  "Tetairoa McMillanCAR"),
    (28,  "Trevor LawrenceJAC"),
    (29,  "Jalen HurtsPHI"),
    (30,  "Colston LovelandCHI"),
    (31,  "Emeka EgbukaTBB"),
    (32,  "Bo NixDEN"),
    (33,  "Jonathan TaylorIND"),
    (34,  "James CookBUF"),
    (35,  "Carnell TateRTEN"),
    (36,  "George PickensDAL"),
    (37,  "Brock PurdySFO"),
    (38,  "Tyler WarrenIND"),
    (39,  "Garrett WilsonNYJ"),
    # 40: 2027 Mid 1st — skipped
    # 41: 2026 Early 1st — skipped
    (42,  "Fernando MendozaRLVR"),
    (43,  "Jordan LoveGBP"),
    (44,  "Nico CollinsHOU"),
    (45,  "Quinshon JudkinsCLE"),
    (46,  "Chris OlaveNOS"),
    (47,  "Rome OdunzeCHI"),
    (48,  "Cam WardTEN"),
    (49,  "Kenneth Walker IIIKCC"),
    (50,  "Breece HallNYJ"),
    (51,  "Ladd McConkeyLAC"),
    (52,  "Jordyn TysonRNOS"),
    (53,  "TreVeyon HendersonNEP"),
    (54,  "Luther BurdenCHI"),
    (55,  "DeVonta SmithPHI"),
    (56,  "Makai LemonRPHI"),
    (57,  "Marvin Harrison Jr.ARI"),
    (58,  "Christian McCaffreySFO"),
    # 59: 2028 Early 1st — skipped
    (60,  "Chase BrownCIN"),
    # 61: 2027 Late 1st — skipped
    (62,  "Dak PrescottDAL"),
    (63,  "Tee HigginsCIN"),
    (64,  "Tyler ShoughNOS"),
    (65,  "Saquon BarkleyPHI"),
    (66,  "Harold FanninCLE"),
    (67,  "C.J. StroudHOU"),
    (68,  "Tucker KraftGBP"),
    (69,  "Brian Thomas Jr.JAC"),
    (70,  "Bucky IrvingTBB"),
    (71,  "Jadarian PriceRSEA"),
    (72,  "A.J. BrownPHI"),
    (73,  "Kyren WilliamsLAR"),
    (74,  "Jaylen WaddleDEN"),
    (75,  "Baker MayfieldTBB"),
    (76,  "Zay FlowersBAL"),
    (77,  "Cam SkatteboNYG"),
    (78,  "Jared GoffDET"),
    (79,  "Jameson WilliamsDET"),
    (80,  "Sam DarnoldSEA"),
    (81,  "Javonte WilliamsDAL"),
    # 82: 2026 Mid 1st — skipped
    (83,  "Sam LaPortaDET"),
    # 84: 2028 Mid 1st — skipped
    (85,  "Travis EtienneNOS"),
    (86,  "KC ConcepcionRCLE"),
    (87,  "Rashee RiceKCC"),
    (88,  "Bryce YoungCAR"),
    (89,  "Kyle PittsATL"),
    (90,  "Kenyon SadiqRNYJ"),
    # 91: 2028 Late 1st — skipped
    (92,  "Alec PierceIND"),
    (93,  "Kyler MurrayMIN"),
    (94,  "Jordan AddisonMIN"),
    (95,  "Daniel JonesIND"),
    (96,  "Derrick HenryBAL"),
    # 97: 2026 Late 1st — skipped
    (98,  "Malik WillisMIA"),
    # 99: 2027 Early 2nd — skipped
    (100, "Bhayshul TutenJAC"),
    (101, "Omar Cooper Jr.RNYJ"),
    (102, "Christian WatsonGBP"),
    (103, "Eli StowersRPHI"),
    (104, "D.J. MooreBUF"),
    (105, "Matthew StaffordLAR"),
    (106, "Matthew GoldenGBP"),
    (107, "Ty SimpsonRLAR"),
    (108, "Kyle MonangaiCHI"),
    (109, "Oronde GadsdenLAC"),
    (110, "Michael WilsonARI"),
    (111, "Josh DownsIND"),
    (112, "Wan'Dale RobinsonTEN"),
    (113, "D'Andre SwiftCHI"),
    (114, "Josh JacobsGBP"),
    (115, "Parker WashingtonJAC"),
    (116, "DK MetcalfPIT"),
    # 117: 2027 Mid 2nd — skipped
    (118, "Terry McLaurinWAS"),
    (119, "Ricky PearsallSFO"),
    (120, "Jayden ReedGBP"),
    (121, "RJ HarveyDEN"),
    (122, "Denzel BostonRCLE"),
    (123, "Travis HunterJAC"),
    (124, "Zach CharbonnetSEA"),
    (125, "David MontgomeryHOU"),
    (126, "Jayden HigginsHOU"),
    (127, "Isaiah LikelyNYG"),
    (128, "Michael PittmanPIT"),
    (129, "Xavier WorthyKCC"),
    (130, "Quentin JohnstonLAC"),
    (131, "Chuba HubbardCAR"),
    (132, "Davante AdamsLAR"),
    # 133: 2026 Early 2nd — skipped
    (134, "Mike EvansSFO"),
    (135, "Blake CorumLAR"),
    (136, "Romeo DoubsNEP"),
    (137, "Dalton KincaidBUF"),
    (138, "George KittleSFO"),
    (139, "Jake FergusonDAL"),
    (140, "Rico DowdlePIT"),
    (141, "Jonathon BrooksCAR"),
    # 142: 2027 Late 2nd — skipped
    # 143: 2028 Early 2nd — skipped
    (144, "Jaylen WarrenPIT"),
    (145, "Courtland SuttonDEN"),
    (146, "Michael Penix Jr.ATL"),
    (147, "Jonah ColemanRDEN"),
    (148, "Jakobi MeyersJAC"),
    (149, "Jalen CokerCAR"),
    (150, "Brenton StrangeJAC"),
    (151, "Chris BellRMIA"),
    (152, "Khalil ShakirBUF"),
    # 153: 2028 Mid 2nd — skipped
    (154, "Antonio WilliamsRWAS"),
    (155, "Jalen McMillanTBB"),
    (156, "J.K. DobbinsDEN"),
    (157, "Chris GodwinTBB"),
    # 158: 2026 Mid 2nd — skipped
    (159, "Germie BernardRPIT"),
    (160, "Nicholas SingletonRTEN"),
    (161, "Jacory Croskey-MerrittWAS"),
    (162, "Rhamondre StevensonNEP"),
    (163, "Rashid ShaheedSEA"),
    (164, "J.J. McCarthyMIN"),
    # 165: 2026 Late 2nd — skipped
    (166, "Kenneth GainwellTBB"),
    # 167: 2028 Late 2nd — skipped
    (168, "Woody MarksHOU"),
    (169, "Isaac TeSlaaDET"),
    (170, "T.J. HockensonMIN"),
    (171, "Elijah SarrattRBAL"),
    (172, "Tre HarrisLAC"),
    (173, "Tony PollardTEN"),
    (174, "AJ BarnerSEA"),
    (175, "Mark AndrewsBAL"),
    (176, "Dylan SampsonCLE"),
    (177, "Shedeur SandersCLE"),
    (178, "Tua TagovailoaATL"),
    (179, "Tyler AllgeierARI"),
    (180, "Chigoziem OkonkwoWAS"),
    (181, "Rachaad WhiteWAS"),
    (182, "Tory HortonSEA"),
    (183, "Jauan JenningsMIN"),
    (184, "Malachi FieldsRNYG"),
    (185, "Jacoby BrissettARI"),
    (186, "Gunnar HelmTEN"),
    (187, "Kayshon BoutteNEP"),
    (188, "Jaylin NoelHOU"),
    (189, "Zachariah BranchRATL"),
    (190, "Tyrone TracyNYG"),
    (191, "Troy FranklinDEN"),
    (192, "Braelon AllenNYJ"),
    (193, "Mac JonesSFO"),
    (194, "Jordan MasonMIN"),
    (195, "Chris Brazzell IIRCAR"),
    (196, "Terrance FergusonLAR"),
    # 197: 2027 Early 3rd — skipped
    (198, "Jerry JeudyCLE"),
    (199, "Tyjae SpearsTEN"),
    (200, "Elic AyomanorTEN"),
]

# Known name mismatches: KTC name (after stripping team) → canonical master name
NAME_MAP = {
    "James Cook":       "James Cook III",
    "Travis Etienne":   "Travis Etienne Jr.",
}


def strip_team(name):
    """Remove trailing all-caps NFL team code (optionally prefixed with R for rookie)."""
    return re.sub(r'\s*R?[A-Z]{2,4}$', '', name).strip()


def normalize(name):
    name = unicodedata.normalize("NFKD", name)
    name = name.encode("ascii", "ignore").decode("ascii")
    name = name.lower()
    name = re.sub(r"\b(jr|sr|ii|iii|iv|v)\b\.?", "", name)
    name = re.sub(r"[^a-z\s]", "", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name


def main():
    # Build cleaned rankings list
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

    # Rename column
    ktc_idx = header.index(OLD_COL)
    header[ktc_idx] = NEW_COL

    # Build name → row index lookup
    name_to_idx = {normalize(row[0]): i for i, row in enumerate(data)}

    # Clear existing KTC rankings
    for row in data:
        row[ktc_idx] = ""

    matched = 0
    unmatched = []

    for rank, name in rankings:
        norm = normalize(name)
        if norm in name_to_idx:
            data[name_to_idx[norm]][ktc_idx] = str(rank)
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
        new_row[ktc_idx] = str(rank)
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
