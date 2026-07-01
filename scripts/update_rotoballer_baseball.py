import csv
import subprocess
import unicodedata
import re

MASTER = "baseball/baseball_rankings_master.csv"
OLD_COL = "RotoWorld (Eric Cross, May 2026)"
NEW_COL = "RotoBaller (Eric Cross, Jun 2026)"

RANKINGS = {
    "Bobby Witt Jr.": 1, "Shohei Ohtani": 2, "Juan Soto": 3, "Corbin Carroll": 4,
    "Elly De La Cruz": 5, "James Wood": 6, "Nick Kurtz": 7, "Junior Caminero": 8,
    "Konnor Griffin": 9, "Jackson Chourio": 10, "Paul Skenes": 11, "Yordan Alvarez": 12,
    "Julio Rodriguez": 13, "Jacob Misiorowski": 14, "Tarik Skubal": 15,
    "Ronald Acuna Jr.": 16, "Fernando Tatis Jr.": 17, "Kevin McGonigle": 18,
    "Aaron Judge": 19, "Ben Rice": 20, "Pete Crow-Armstrong": 21, "CJ Abrams": 22,
    "Chase Burns": 23, "Jordan Walker": 24, "Cam Schlittler": 25, "Brice Turang": 26,
    "Cristopher Sanchez": 27, "Yoshinobu Yamamoto": 28, "Sal Stewart": 29,
    "Garrett Crochet": 30, "JJ Wetherholt": 31, "Roman Anthony": 32, "Miguel Vargas": 33,
    "Kyle Tucker": 34, "Gunnar Henderson": 35, "Jose Ramirez": 36,
    "Vladimir Guerrero Jr.": 37, "Drake Baldwin": 38, "Jazz Chisholm Jr.": 39,
    "Bryan Woo": 40, "Kyle Schwarber": 41, "Francisco Lindor": 42, "Nolan McLean": 43,
    "Jesus Made": 44, "Logan Gilbert": 45, "Matt Olson": 46, "Ketel Marte": 47,
    "Hunter Brown": 48, "Pete Alonso": 49, "Shea Langeliers": 50, "Joe Ryan": 51,
    "Oneil Cruz": 52, "Travis Bazzana": 53, "Bryce Eldridge": 54, "Samuel Basallo": 55,
    "Andy Pages": 56, "Hunter Greene": 57, "Wyatt Langford": 58, "Riley Greene": 59,
    "Bryce Harper": 60, "Dylan Cease": 61, "Eury Perez": 62, "Mason Miller": 63,
    "Josue De Paula": 64, "Cole Ragans": 65, "Michael Harris II": 66, "Kade Anderson": 67,
    "Leo De Vries": 68, "Randy Arozarena": 69, "Max Fried": 70, "Maikel Garcia": 71,
    "Cody Bellinger": 72, "Zach Neto": 73, "Max Clark": 74, "Logan Webb": 75,
    "Munetaka Murakami": 76, "Byron Buxton": 77, "Spencer Schwellenbach": 78,
    "Jesus Luzardo": 79, "George Kirby": 80, "Jeremy Pena": 81, "Tyler Soderstrom": 82,
    "Rafael Devers": 83, "Kyle Bradish": 84, "Josh Naylor": 85, "Payton Tolle": 86,
    "Jac Caglianone": 87, "Otto Lopez": 88, "Chase DeLauter": 89, "Braxton Ashcraft": 90,
    "Brent Rooker": 91, "Hunter Goodman": 92, "Freddy Peralta": 93, "Jackson Merrill": 94,
    "Alec Burleson": 95, "Gavin Williams": 96, "Sam Antonacci": 97, "Trey Yesavage": 98,
    "Eli Willits": 99, "Dillon Dingler": 100, "Mike Sirota": 101, "Jonathan Aranda": 102,
    "Corey Seager": 103, "William Contreras": 104, "Ozzie Albies": 105,
    "Tyler Glasnow": 106, "Michael Busch": 107, "Seiya Suzuki": 108,
    "Framber Valdez": 109, "Cal Raleigh": 110, "Colson Montgomery": 111,
    "Bryce Miller": 112, "Seth Hernandez": 113, "Ceddanne Rafaela": 114,
    "Jackson Holliday": 115, "Ivan Herrera": 116, "Walker Jenkins": 117,
    "Manny Machado": 118, "Carson Benge": 119, "Edward Florentino": 120,
    "Bo Bichette": 121, "Kyle Stowers": 122, "Parker Messick": 123, "Colt Emerson": 124,
    "Kyle Harrison": 125, "Zyhir Hope": 126, "Ryan Waldschmidt": 127, "Mookie Betts": 128,
    "Bubba Chandler": 129, "Rainiel Rodriguez": 130, "Vinnie Pasquantino": 131,
    "Trea Turner": 132, "Yandy Diaz": 133, "Connelly Early": 134, "Kazuma Okamoto": 135,
    "Ranger Suarez": 136, "Willy Adames": 137, "Drew Rasmussen": 138, "Jhoan Duran": 139,
    "Geraldo Perdomo": 140, "Michael King": 141, "Sandy Alcantara": 142,
    "Wilyer Abreu": 143, "Joshua Baez": 144, "Franklin Arias": 145, "Pablo Lopez": 146,
    "Brandon Nimmo": 147, "Blake Snell": 148, "Christian Yelich": 149, "Josh Hader": 150,
    "Austin Riley": 151, "Thomas White": 152, "Henry Bolte": 153, "Jared Jones": 154,
    "Carter Jensen": 155, "Ryan Pepiot": 156, "Jo Adell": 157, "Brandon Lowe": 158,
    "Bryce Elder": 159, "Adley Rutschman": 160, "Roki Sasaki": 161,
    "Shota Imanaga": 162, "Nico Hoerner": 163, "Casey Schmitt": 164,
    "Shane McClanahan": 165, "Will Smith": 166, "A.J. Ewing": 167, "Caleb Bonemer": 168,
    "Spencer Strider": 169, "Ian Happ": 170, "Kaelen Culpepper": 171, "Jake Bauers": 172,
    "Sebastian Walcott": 173, "Aidan Miller": 174, "MacKenzie Gore": 175,
    "Jake McCarthy": 176, "Ryan Sloan": 177, "Jacob Wilson": 178, "Bryan Reynolds": 179,
    "Ben Brown": 180, "Luis Pena": 181, "Carlos Rodon": 182, "Daylen Lile": 183,
    "TJ Rumfield": 184, "Cade Horton": 185, "Xavier Edwards": 186, "Freddie Freeman": 187,
    "Tatsuya Imai": 188, "Luis Garcia Jr.": 189, "Tanner Bibee": 190, "Taylor Ward": 191,
    "Luis Robert Jr.": 192, "Nick Pivetta": 193, "Max Meyer": 194, "Eric Hartman": 195,
    "Gage Jump": 196, "Andrew Fischer": 197, "Braden Montgomery": 198,
    "Theo Gillen": 199, "Anthony Eyanson": 200,
}


def normalize(name):
    name = unicodedata.normalize("NFKD", name)
    name = name.encode("ascii", "ignore").decode("ascii")
    name = name.lower()
    name = re.sub(r"\b(jr|sr|ii|iii|iv|v)\b\.?", "", name)
    name = re.sub(r"[^a-z\s]", "", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name


norm_rankings = {normalize(k): v for k, v in RANKINGS.items()}

with open(MASTER, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    fieldnames = list(reader.fieldnames)
    rows = list(reader)

# Rename column
if OLD_COL in fieldnames:
    idx = fieldnames.index(OLD_COL)
    fieldnames[idx] = NEW_COL
    for row in rows:
        row[NEW_COL] = row.pop(OLD_COL)
    print(f"Renamed '{OLD_COL}' → '{NEW_COL}'.")
elif NEW_COL not in fieldnames:
    insert_before = "Average Rank"
    idx = fieldnames.index(insert_before)
    fieldnames = fieldnames[:idx] + [NEW_COL] + fieldnames[idx:]
    print(f"Added new column '{NEW_COL}'.")

# Clear existing values for this source
for row in rows:
    row[NEW_COL] = ""

# Match existing players
existing_norm = {normalize(row["Player"]): row for row in rows}
matched = 0
unmatched = []
for name, rank in RANKINGS.items():
    key = normalize(name)
    if key in existing_norm:
        existing_norm[key][NEW_COL] = rank
        matched += 1
    else:
        unmatched.append((name, rank))

print(f"Matched {matched} / {len(RANKINGS)} players.")

# Add new players
for name, rank in unmatched:
    new_row = {col: "" for col in fieldnames}
    new_row["Player"] = name
    new_row[NEW_COL] = rank
    rows.append(new_row)
    print(f"  Added new player: {name} (rank {rank})")

with open(MASTER, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("Running recalculate.py...")
subprocess.run(["python3", "scripts/recalculate.py", MASTER], check=True)
print("Done.")
