import json
import os

# ---------------- CONFIG ----------------

cats = [
    "222","333","333bf","333fm","333oh",
    "444","444bf","555","555bf",
    "666","777","clock","minx","pyram","skewb","sq1","333mbf"
]

single_events = ["333bf", "444bf", "555bf", "333fm", "333mbf"]

single_or_mean = ["333bf", "444bf", "555bf", "333fm"]

rankings_avg_folder = "./../cubing-peru-api-v0/Rankings/average"
rankings_single_folder = "./../cubing-peru-api-v0/Rankings/single"
output_file = "./../cubing-peru-api-v0/KinchRank/results_kinch_rank.json"

# ---------------- HELPERS ----------------

def load_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def safe_int(v):
    try:
        return int(v)
    except:
        return None

# ---------------- LOAD ----------------

rankings_avg = {cat: load_json(f"{rankings_avg_folder}/{cat}.json") for cat in cats}
rankings_single = {cat: load_json(f"{rankings_single_folder}/{cat}.json") for cat in cats}

# ---------------- BASES (NR Perú) ----------------

event_bases = {}
event_bases_mean = {}

for cat in cats:
    data = rankings_single[cat]
    if data:
        b = safe_int(data[0].get("best"))
        if b:
            event_bases[cat] = b
    data_mean = rankings_avg[cat]
    if data_mean:
        b = safe_int(data_mean[0].get("average"))
        if b:
            event_bases_mean[cat] = b

# ---------------- PERSONAS ----------------

persons = set()
for cat in cats:
    for r in rankings_avg.get(cat, []):
        if r.get("person_id"):
            persons.add(r["person_id"])
    for r in rankings_single.get(cat, []):
        if r.get("person_id"):
            persons.add(r["person_id"])

# ---------------- CALCULO ----------------

results = []

for pid in persons:
    person_name = ""
    gender = ""
    country = ""

    kinchSum = 0.0
    categories = []

    for cat in cats:
        base = event_bases.get(cat)  # NR SINGLE
        base_mean = event_bases_mean.get(cat)  # NR MEAN

        record = None
        personal = None
        personal_mean = None

        if cat == '333mbf':
            recs = [r for r in rankings_single[cat] if r["person_id"] == pid]
            if recs:
                record = recs[0]
                personal = safe_int(record.get("best"))
        elif cat in single_or_mean:
            recs_single = [r for r in rankings_single[cat] if r["person_id"] == pid]
            if recs_single:
                record = recs_single[0]
                personal = safe_int(record.get("best"))

            recs = [r for r in rankings_avg[cat] if r["person_id"] == pid]
            if recs:
                record = recs[0]
                personal_mean = safe_int(record.get("average"))
        else:
            recs = [r for r in rankings_avg[cat] if r["person_id"] == pid]
            if recs:
                record = recs[0]
                personal_mean = safe_int(record.get("average"))

        # Guardar nombre de una vez
        if record and not person_name:
            person_name = record.get("person_name", "")
            gender = record.get("gender", "")
            country = record.get("competitionCountryIso", "")

        # ---- kinch por evento ----
        kinch_event = 0.0
        if base:
            if cat == "333mbf" and personal:
                points_base = 99 - round(base / 10000000, 0)
                points_personal = 99 - round(personal / 10000000, 0)

                time_base = round(base / 100, 0) - (99 - points_base) * 100000
                time_personal = round(personal / 100, 0) - (99 - points_personal) * 100000

                prop_hour_left_base = 1 - time_base / 3600
                prop_hour_left_personal = 1 - time_personal / 3600

                kinch_event = round((points_personal + prop_hour_left_personal) / (points_base + prop_hour_left_base) * 100, 2)
            elif (cat in single_or_mean):
                #VALIDAMOS EL MAS CERCANO A NR
                if personal_mean and personal_mean > 0:
                    kinch_event = max(round((base / personal) * 100, 2), round((base_mean / personal_mean) * 100, 2))
                elif personal:
                    kinch_event = round((base / personal) * 100, 2)
            elif personal_mean and personal_mean > 0:
                kinch_event = round((base_mean / personal_mean) * 100, 2)

        kinchSum += kinch_event

        categories.append({
            "eventId": cat,
            "best": str(personal) if personal else None,
            "competitionId": record.get("competition_id") if record else None,
            "competitionName": record.get("competitionName") if record else None,
            "competitionCountryIso": record.get("competitionCountryIso") if record else None,
            "countryRank": int(record.get("countryRank")) if record and record.get("countryRank") else None,
            "kinch": kinch_event
        })

    kinchAvg = round(kinchSum / len(cats), 2)

    if round(kinchSum, 2) != 0.0:
        results.append({
            "personName": person_name,
            "personId": pid,
            "gender": gender,
            "countryIso": country,
            "kinchAvg": kinchAvg,
            "kinchSum": round(kinchSum, 2),
            "categories": categories
        })

# ---------------- ORDENAR Y GUARDAR ----------------

results.sort(key=lambda x: x["kinchAvg"], reverse=True)

os.makedirs(os.path.dirname(output_file), exist_ok=True)

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("✅ Kinch Rank generado correctamente")
