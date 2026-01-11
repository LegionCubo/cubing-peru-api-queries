import json
import os

cats = ["222","333","333bf", "333fm", "333ft", "333mbf", "333mbo", "333oh","444", "444bf", "555", "555bf", "666", "777", "clock", "magic", "minx", "mmagic", "pyram", "skewb", "sq1"]

# 📌 Cargar persons en memoria (para lookup rápido)
persons_file = "./../cubing-peru-api-v0/Persons/persons.json"
with open(persons_file, "r", encoding="utf-8") as f:
    persons = {p["wca_id"]: p for p in json.load(f)}

def make_ranking(input_folder, output_folder, field):
    os.makedirs(output_folder, exist_ok=True)

    for cat in cats:
        input_file = f"{input_folder}/{cat}.json"
        if not os.path.exists(input_file):
            continue

        # diccionario: personId → mejor record completo
        best_by_person = {}

        with open(input_file, "r", encoding="utf-8") as f:
            results = json.load(f)
            for record in results:
                value = int(record.get(field, -1))
                if value > 0:  # ignorar DNF (-1, 0)
                    pid = record.get("person_id")

                    # si no existe o es mejor → guardamos todo el record
                    if pid not in best_by_person or value < int(best_by_person[pid].get(field, float("inf"))):
                        best_by_person[pid] = record

                        # añadir gender desde persons.json
                        person = persons.get(pid, {})
                        record["gender"] = person.get("gender", "")

        # ranking = todos los mejores records
        ranking = list(best_by_person.values())

        # ordenar por campo (best o average)
        ranking.sort(key=lambda r: int(r.get(field, float("inf"))))

        # guardar
        output_file = f"{output_folder}/{cat}.json"
        with open(output_file, "w", encoding="utf-8") as out:
            json.dump(ranking, out, ensure_ascii=False, indent=2)

        print(f"✅ Ranking generado para {cat} ({field})")

# 📌 Generar rankings para single y average
make_ranking("./../cubing-peru-api-v0/Results/single", "./../cubing-peru-api-v0/Rankings/single", "best")
make_ranking("./../cubing-peru-api-v0/Results/average", "./../cubing-peru-api-v0/Rankings/average", "average")
