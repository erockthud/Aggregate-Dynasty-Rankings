import csv
import subprocess
import unicodedata
import re

MASTER = "baseball/baseball_rankings_master.csv"
SOURCE_COL = "Dynasty Dugout (Jun 2026)"

RANKINGS = {
    "Shohei Ohtani": 1,
    "Elly De La Cruz": 2,
    "Juan Soto": 3,
    "Bobby Witt Jr.": 4,
    "Aaron Judge": 5,
    "Corbin Carroll": 6,
    "Julio Rodriguez": 7,
    "Ronald Acuna Jr.": 8,
    "Yordan Alvarez": 9,
    "Paul Skenes": 10,
    "Tarik Skubal": 11,
    "Junior Caminero": 12,
    "James Wood": 13,
    "Konnor Griffin": 14,
    "Kevin McGonigle": 15,
    "Nick Kurtz": 16,
    "Jacob Misiorowski": 17,
    "Vladimir Guerrero Jr.": 18,
    "Gunnar Henderson": 19,
    "Kyle Tucker": 20,
    "Jackson Chourio": 21,
    "Jose Ramirez": 22,
    "Fernando Tatis Jr.": 23,
    "CJ Abrams": 24,
    "Cristopher Sanchez": 25,
    "Yoshinobu Yamamoto": 26,
    "Zach Neto": 27,
    "Matt Olson": 28,
    "Ben Rice": 29,
    "Francisco Lindor": 30,
    "JJ Wetherholt": 31,
    "Kyle Schwarber": 32,
    "Cam Schlittler": 33,
    "Garrett Crochet": 34,
    "Bryce Harper": 35,
    "Jazz Chisholm Jr.": 36,
    "Oneil Cruz": 37,
    "Ketel Marte": 38,
    "Chase Burns": 39,
    "Jesus Made": 40,
    "Trea Turner": 41,
    "Roman Anthony": 42,
    "Pete Alonso": 43,
    "Brice Turang": 44,
    "Logan Gilbert": 45,
    "Manny Machado": 46,
    "Riley Greene": 47,
    "Andy Pages": 48,
    "Bryan Woo": 49,
    "Jacob deGrom": 50,
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
    fieldnames = reader.fieldnames
    rows = list(reader)

if SOURCE_COL in fieldnames:
    print(f"Column '{SOURCE_COL}' already exists — updating values.")
else:
    insert_before = "Average Rank"
    idx = fieldnames.index(insert_before)
    fieldnames = list(fieldnames[:idx]) + [SOURCE_COL] + list(fieldnames[idx:])
    print(f"Added new column '{SOURCE_COL}'.")

matched = 0
for row in rows:
    key = normalize(row["Player"])
    if key in norm_rankings:
        row[SOURCE_COL] = norm_rankings[key]
        matched += 1
    elif SOURCE_COL not in row:
        row[SOURCE_COL] = ""

print(f"Matched {matched} / {len(RANKINGS)} players.")

with open(MASTER, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("Running recalculate.py...")
subprocess.run(["python3", "scripts/recalculate.py", MASTER], check=True)
print("Done.")
