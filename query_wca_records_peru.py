import json
import os

# Categorías oficiales
cats = ["222","333","333bf","333fm","333oh","444","444bf","555","555bf","666","777","clock","minx","pyram","skewb","sq1","333mbf"]

# Directorios
BASE_DIR = "./../cubing-peru-api-v0/Results"
SINGLE_DIR = os.path.join(BASE_DIR, "single")
AVERAGE_DIR = os.path.join(BASE_DIR, "average")
OUTPUT_DIR = "./../cubing-peru-api-v0/Records"

# Crear directorio de salida
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -----------------------------------------
# Obtener TODOS los mejores resultados (empates incluidos)
# -----------------------------------------
def get_all_best(data, mode):
    if not data:
        return []

    best_value = data[0].get(mode)

    # Filtrar todos los que empatan con el mejor valor
    best_list = [d for d in data if d.get(mode) == best_value]

    result = []
    for d in best_list:
        result.append({
            "personId": d.get("personId"),
            "personName": d.get("personName"),
            mode: d.get(mode),
            "competitionId": d.get("competitionId"),
            "competitionName": d.get("competitionName"),
            "competitionCountryIso": d.get("competitionCountryIso"),
            "gender": d.get("gender"),
            "times": [
                d.get("value1"),
                d.get("value2"),
                d.get("value3"),
                d.get("value4"),
                d.get("value5"),
            ],
        })

    return result

# -----------------------------------------
# Obtener TODOS los mejores resultados por género
# -----------------------------------------
def get_all_best_by_gender(data, gender, mode):
    filtered = [d for d in data if d.get("gender") == gender]

    if not filtered:
        return []

    best_value = filtered[0].get(mode)
    best_list = [d for d in filtered if d.get(mode) == best_value]

    result = []
    for d in best_list:
        result.append({
            "personId": d.get("personId"),
            "personName": d.get("personName"),
            mode: d.get(mode),
            "competitionId": d.get("competitionId"),
            "competitionName": d.get("competitionName"),
            "competitionCountryIso": d.get("competitionCountryIso"),
            "times": [
                d.get("value1"),
                d.get("value2"),
                d.get("value3"),
                d.get("value4"),
                d.get("value5"),
            ],
        })

    return result

# -----------------------------------------
# Construir archivo best_records.json
# -----------------------------------------
def build_best_records():
    result = {}

    for cat in cats:
        cat_entry = {"m": {}, "f": {}}

        single_path = os.path.join(SINGLE_DIR, f"{cat}.json")
        average_path = os.path.join(AVERAGE_DIR, f"{cat}.json")

        # Cargar data
        single_data = []
        average_data = []

        if os.path.exists(single_path):
            with open(single_path, "r", encoding="utf-8") as f:
                single_data = json.load(f)

        if os.path.exists(average_path):
            with open(average_path, "r", encoding="utf-8") as f:
                average_data = json.load(f)

        # Mejor(es) general single
        best_single = get_all_best(single_data, "best")
        if best_single:
            cat_entry["single"] = best_single

        # Mejor(es) general average
        best_average = get_all_best(average_data, "average")
        if best_average:
            cat_entry["average"] = best_average

        # Mejor(es) masculino single / average
        cat_entry["m"]["single"] = get_all_best_by_gender(single_data, "m", "best")
        cat_entry["m"]["average"] = get_all_best_by_gender(average_data, "m", "average")

        # Mejor(es) femenino single / average
        cat_entry["f"]["single"] = get_all_best_by_gender(single_data, "f", "best")
        cat_entry["f"]["average"] = get_all_best_by_gender(average_data, "f", "average")

        result[cat] = cat_entry

    # Guardar archivo final
    output_path = os.path.join(OUTPUT_DIR, "best_records.json")

    with open(output_path, "w", encoding="utf-8") as out:
        json.dump(result, out, ensure_ascii=False, indent=2)

    print(f"✅ Archivo generado: {output_path}")

# -----------------------------------------
if __name__ == "__main__":
    build_best_records()
