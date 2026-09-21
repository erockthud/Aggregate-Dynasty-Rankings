#!/usr/bin/env python3
"""Update Dizzle Dynasty basketball rankings: rename from Pts Apr 2026 to Pts Sep 2026,
replace all values, and backfill Position/Team/Age for rows currently missing them."""

import csv
import re
import unicodedata
import subprocess

MASTER_PATH = "basketball/basketball_rankings_master.csv"
RAW_PATH = "/tmp/claude-1000/-workspaces-Aggregate-Dynasty-Rankings/5c2283e2-e7da-4266-8f4c-62ffe5767895/scratchpad/dizzle_raw.txt"
OLD_COL = "Dizzle Dynasty (Pts, Apr 2026)"
NEW_COL = "Dizzle Dynasty (Pts, Sep 2026)"

# Source name (normalized) -> canonical normalized name in master.
# Same quirks as the Apr 2026 Dizzle source (typos/variants).
NAME_MAP = {
    "carlton carrington": "bub carrington",
    "ron holland":        "ronald holland",
    "khaman malauch":     "khaman maluach",
    "ayo dosumnu":        "ayo dosunmu",
    "terrance shannon":   "terrence shannon",
}

TEAM_MAP = {
    "PHO": "PHX",
}

NBA_TEAMS = {
    "ATL","BKN","BOS","CHA","CHI","CLE","DAL","DEN","DET","GSW",
    "HOU","IND","LAC","LAL","MEM","MIA","MIL","MIN","NOP","NYK",
    "OKC","ORL","PHI","PHX","POR","SAC","SAS","TOR","UTA","WAS",
}


def normalize(name):
    name = unicodedata.normalize("NFKD", name)
    name = name.encode("ascii", "ignore").decode("ascii")
    name = name.lower()
    name = re.sub(r"\b(jr|sr|ii|iii|iv|v)\b\.?", "", name)
    name = re.sub(r"[^a-z\s]", "", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name


def parse_player_name(raw):
    """Extract player name from draft-pick format '1.01 / Player Name', or return as-is."""
    if " / " in raw:
        return raw.split(" / ", 1)[1].strip()
    return raw.strip()


def parse_team(raw):
    """Take the post-trade team if an arrow is present; map free agents to blank."""
    team = raw.strip()
    if " -> " in team:
        team = team.split(" -> ", 1)[1].strip()
    team = TEAM_MAP.get(team, team)
    if team == "FA":
        return ""
    return team


def parse_position(raw):
    """Map the first listed position to the master's G/F/C convention."""
    first = raw.split("/")[0].strip()
    return {"PG": "G", "SG": "G", "SF": "F", "PF": "F", "C": "C"}.get(first, "")


def parse_age(raw):
    """Floor a decimal age string to an integer to match the master's convention."""
    try:
        return str(int(float(raw)))
    except ValueError:
        return ""


def load_raw():
    rows = []
    with open(RAW_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip() or "TIER BREAK" in line:
                continue
            parts = line.split("\t")
            if len(parts) < 6:
                continue
            rank_str, name_raw, pos_raw, team_raw, _dob, age_raw = parts[:6]
            rank = int(rank_str)
            name = parse_player_name(name_raw)
            rows.append((rank, name, pos_raw.strip(), team_raw.strip(), age_raw.strip()))
    return rows


def main():
    dizzle_rows = load_raw()
    print(f"Parsed {len(dizzle_rows)} rows from source")

    dizzle_lookup = {}
    for rank, name, pos_raw, team_raw, age_raw in dizzle_rows:
        key = normalize(name)
        mapped_key = NAME_MAP.get(key, key)
        dizzle_lookup[mapped_key] = (rank, name, pos_raw, team_raw, age_raw)

    with open(MASTER_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        old_fieldnames = list(reader.fieldnames)
        rows = list(reader)

    new_fieldnames = [NEW_COL if fn == OLD_COL else fn for fn in old_fieldnames]

    matched_keys = set()
    backfilled = []
    for row in rows:
        row[NEW_COL] = row.pop(OLD_COL, "")
        key = normalize(row["Player"])
        if key in dizzle_lookup:
            rank, _, pos_raw, team_raw, age_raw = dizzle_lookup[key]
            row[NEW_COL] = rank
            matched_keys.add(key)

            changed = False
            if not row.get("Position"):
                pos = parse_position(pos_raw)
                if pos:
                    row["Position"] = pos
                    changed = True
            if not row.get("Team"):
                team = parse_team(team_raw)
                if team:
                    row["Team"] = team
                    if not row.get("Level"):
                        row["Level"] = "NBA" if team in NBA_TEAMS else "College"
                    changed = True
            if not row.get("Age"):
                age = parse_age(age_raw)
                if age:
                    row["Age"] = age
                    changed = True
            if changed:
                backfilled.append(row["Player"])
        else:
            row[NEW_COL] = ""

    unmatched = []
    for rank, name, pos_raw, team_raw, age_raw in dizzle_rows:
        key = normalize(name)
        mapped_key = NAME_MAP.get(key, key)
        if mapped_key not in matched_keys:
            unmatched.append((rank, name, pos_raw, team_raw, age_raw))

    print(f"Matched: {len(matched_keys)} players")
    print(f"Backfilled Position/Team/Age for {len(backfilled)} existing rows: {backfilled}")
    print(f"New players to add: {len(unmatched)}")
    for rank, name, pos_raw, team_raw, age_raw in unmatched:
        print(f"  [{rank}] {name} ({pos_raw}, {team_raw})")

    for rank, name, pos_raw, team_raw, age_raw in unmatched:
        team = parse_team(team_raw)
        level = "NBA" if team in NBA_TEAMS else "College"
        new_row = {fn: "" for fn in new_fieldnames}
        new_row["Player"] = name
        new_row["Position"] = parse_position(pos_raw)
        new_row["Team"] = team
        new_row["Age"] = parse_age(age_raw)
        new_row["Level"] = level
        new_row[NEW_COL] = rank
        rows.append(new_row)

    with open(MASTER_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=new_fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nWrote {len(rows)} rows to {MASTER_PATH}")

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
