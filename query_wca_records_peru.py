import json
import os

# Categorías conocidas
cats = ["222","333","333bf","333fm","333oh","444","444bf","555","555bf","666","777","clock","minx","pyram","skewb","sq1", "333mbf"]

# Directorios base
BASE_DIR = "./../cubing-peru-api-v0/Rankings"
SINGLE_DIR = os.path.join(BASE_DIR, "single")
AVERAGE_DIR = os.path.join(BASE_DIR, "average")
OUTPUT_DIR = "./../cubing-peru-api-v0/Records"

# Asegurar carpeta de salida
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Función para obtener el mejor resultado (posición 1)
def get_best(data):
    if not data:
        return None
    best = data[0]
    return {
        "personId": best.get("personId"),
        "personName": best.get("personName"),
        "best": best.get("best"),
        "average": best.get("average"),
        "competitionId": best.get("competitionId"),
        "competitionName": best.get("competitionName"),
        "competitionCountryIso": best.get("competitionCountryIso"),
        "gender": best.get("gender"),
        "times": [
            best.get("value1"),
            best.get("value2"),
            best.get("value3"),
            best.get("value4"),
            best.get("value5"),
        ],
    }

# Función para obtener el mejor resultado por género
def get_best_by_gender(data, gender, mode):
    filtered = [d for d in data if d.get("gender") == gender]
    if not filtered:
        return None
    best = filtered[0]  # ya está ordenado del mejor al peor
    return {
        "personId": best.get("personId"),
        "personName": best.get("personName"),
        mode: best.get(mode),
        "competitionId": best.get("competitionId"),
        "competitionName": best.get("competitionName"),
        "competitionCountryIso": best.get("competitionCountryIso"),
        "times": [
            best.get("value1"),
            best.get("value2"),
            best.get("value3"),
            best.get("value4"),
            best.get("value5"),
        ],
    }

# Función principal
def build_best_records():
    result = {}

    for cat in cats:
        cat_entry = {"m": {}, "f": {}}

        # Rutas
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

        # --- Mejor general single ---
        best_single = get_best(single_data)
        if best_single:
            cat_entry["single"] = {
                "personId": best_single["personId"],
                "personName": best_single["personName"],
                "best": best_single["best"],
                "competitionId": best_single["competitionId"],
                "competitionName": best_single["competitionName"],
                "competitionCountryIso": best_single["competitionCountryIso"],
                "times": best_single["times"],
            }

        # --- Mejor general average ---
        best_average = get_best(average_data)
        if best_average:
            cat_entry["average"] = {
                "personId": best_average["personId"],
                "personName": best_average["personName"],
                "average": best_average["average"],
                "competitionId": best_average["competitionId"],
                "competitionName": best_average["competitionName"],
                "competitionCountryIso": best_average["competitionCountryIso"],
                "times": best_average["times"],
            }

        # --- Mejor masculino/femenino single ---
        best_m_single = get_best_by_gender(single_data, "m", "best")
        best_f_single = get_best_by_gender(single_data, "f", "best")

        if best_m_single:
            cat_entry["m"]["single"] = best_m_single
        if best_f_single:
            cat_entry["f"]["single"] = best_f_single

        # --- Mejor masculino/femenino average ---
        best_m_average = get_best_by_gender(average_data, "m", "average")
        best_f_average = get_best_by_gender(average_data, "f", "average")

        if best_m_average:
            cat_entry["m"]["average"] = best_m_average
        if best_f_average:
            cat_entry["f"]["average"] = best_f_average

        result[cat] = cat_entry

    # Guardar en archivo final
    output_path = os.path.join(OUTPUT_DIR, "best_records.json")
    with open(output_path, "w", encoding="utf-8") as out:
        json.dump(result, out, ensure_ascii=False, indent=2)

    print(f"✅ Archivo generado: {output_path}")

if __name__ == "__main__":
    build_best_records()
