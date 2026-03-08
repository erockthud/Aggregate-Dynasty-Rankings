#!/usr/bin/env python3
"""
Recalculate Average Rank and Rank Variance for any sport's rankings_master.csv.

Usage:
    python3 scripts/recalculate.py baseball/baseball_rankings_master.csv
    python3 scripts/recalculate.py hockey/hockey_rankings_master.csv

Rank Variance formula: CoV = STDDEV / (mean + 5)
"""

import csv
import math
import sys

FIXED_COLS = {'Player', 'Position', 'Team', 'Age', 'Level', 'ETA', 'Average Rank', 'Rank Variance'}


def recalculate(path):
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    source_cols = [c for c in fieldnames if c not in FIXED_COLS]

    if not source_cols:
        print(f"No source columns found in {path}. Add ranking source columns first.")
        return

    updated = 0
    for row in rows:
        vals = [float(row[c]) for c in source_cols if row.get(c, '').strip() != '']
        if len(vals) >= 2:
            mean = sum(vals) / len(vals)
            std = math.sqrt(sum((v - mean) ** 2 for v in vals) / (len(vals) - 1))
            row['Average Rank'] = round(mean, 4)
            row['Rank Variance'] = round(std / (mean + 5), 4)
            updated += 1
        elif len(vals) == 1:
            row['Average Rank'] = round(vals[0], 4)
            row['Rank Variance'] = ''

    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Updated {updated} rows in {path}")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 scripts/recalculate.py <path/to/rankings_master.csv>")
        sys.exit(1)
    recalculate(sys.argv[1])
