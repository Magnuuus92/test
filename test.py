import csv
import re
from collections import Counter

INPUT = "companies.csv"
SEP = ","
ENCODING = "utf-8"

exclude_words = ["sport", "klubb", "fotball", "AS", "IK", "idrettslag", "idrettsforening", "idrett", "kommune", "kontor", "ltd", "advokat", "transport", "kvinner", "herrer", "idrettsråd", "Telemark", "Skien", "FF", "ASA", "ANS", "skole", "SA", "GS", "Forening", "Academy", "akademi", "AIL", "IKS", "Kreativ", "ENK", "Holding", "forening", "stiftelse", "NUF"]

pattern = re.compile(
    r"\b(?:" + "|".join(map(re.escape, exclude_words)) + r")\b",
re.IGNORECASE,
)

with open(INPUT, newline="", encoding=ENCODING) as f:
    reader = csv.DictReader(f, delimiter=SEP)
    fieldnames = reader.fieldnames
    rows = list(reader)

print("Columns found:", fieldnames)

def write_csv(path, data):
            with open(path, "w", newline="", encoding="utf-8-sig") as f:
                w = csv.DictWriter(f, fieldnames=fieldnames, delimiter=SEP)
                w.writeheader()
                w.writerows(data)

kept, removed = [], []
for row in rows:
        name = row.get("Navn") or ""
        (removed if pattern.search(name) else kept).append(row)

print(f"Total: {len(rows)}, removed: {len(removed)}, remaining: {len(kept)}")

write_csv("companies_filtered.csv", kept)
write_csv("companies_removed.csv", removed)

odd_chars = re.compile(r"[0-9]|[^\w\s.,&'\-/()]")

def is_suspicious(name):
    return(
        bool(odd_chars.search(name))
        or "  " in name
        or name != name.strip()
        or name.isupper()
        or name.islower()
        or len(name) < 3
    )



suspicious = [r for r in kept if is_suspicious(r.get("Navn") or "")]
write_csv("suspicious.csv", suspicious)

counts = Counter((r.get("Navn") or "").strip().lower() for r in kept)
dupes = [r for r in kept if counts[(r.get("Navn") or "").strip().lower()] > 1]
dupes.sort(key=lambda r: (r.get("Navn") or "").lower())
write_csv("duplicates.csv", dupes)

print(f"Suspicious: {len(suspicious)}, Possible duplicates: {len(dupes)}")