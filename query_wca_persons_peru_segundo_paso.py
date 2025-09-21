import json
import ijson

persons_file = "./../cubing-peru-api-v0/Persons/persons.json"
results_file = "./../cubing-peru-api-v0/Results/results.json"
competitions_file = "./../cubing-peru-api-v0/Competitions/competitions.json"

# 📌 Cargar persons y competitions
with open(persons_file, "r", encoding="utf-8") as f:
    persons = {p["id"]: p for p in json.load(f)}

with open(competitions_file, "r", encoding="utf-8") as f:
    competitions = {c["id"]: c for c in json.load(f)}

last_competition = {}
podiums = {pid: 0 for pid in persons}

# 📌 Procesar results
with open(results_file, "rb") as f:
    for record in ijson.items(f, "item"):
        pid = record.get("personId")
        comp_id = record.get("competitionId")
        round_type = record.get("roundTypeId")
        pos = record.get("pos")

        if not pid or not comp_id:
            continue

        # ---- Última competencia ----
        comp = competitions.get(comp_id, {})
        comp_date = comp.get("competitionDate", "9999-99-99")

        if pid not in last_competition or comp_date > last_competition[pid]["competitionDate"]:
            last_competition[pid] = {
                "competitionId": comp_id,
                "competitionName": comp.get("name", ""),
                "cityName": comp.get("cityName", ""),
                "competitionDate": comp_date,
            }

        # ---- Contar podios (total) ----
        if round_type in ("f", "c") and pos in ("1", "2", "3"):
            podiums[pid] += 1

# 📌 Actualizar persons.json
for pid, person in persons.items():
    person["lastCompetition"] = last_competition.get(pid, None)
    person["podiums"] = podiums.get(pid, 0)

# 📂 Guardar sobrescribiendo persons.json
with open(persons_file, "w", encoding="utf-8") as f:
    json.dump(list(persons.values()), f, ensure_ascii=False, indent=2)

print("✅ persons.json actualizado con la última competencia y total de podios")
