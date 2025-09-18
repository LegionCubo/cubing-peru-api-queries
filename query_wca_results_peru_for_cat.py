import ijson
import json
import os

cats = ["222","333","333bf", "333fm", "333ft", "333mbf", "333mbo", "333oh","444", "444bf", "555", "555bf", "666", "777", "clock", "magic", "minx", "mmagic", "pyram", "skewb", "sq1"]

input_file = "./../cubing-peru-api-v0/Results/results.json"

for cat in cats:
    folder = f"./../cubing-peru-api-v0/Results/{cat}"

    os.makedirs(folder, exist_ok=True)  # crea la carpeta si no existe

    output_file = f"{folder}/{cat}.json"

    with open(input_file, "rb") as f, open(output_file, "w", encoding="utf-8") as out:
        out.write("[\n")
        first = True
        for record in ijson.items(f, "item"):  # cada objeto del array principal
            if record.get("eventId") == cat:
                if not first:
                    out.write(",\n")
                json.dump(record, out, ensure_ascii=False)
                first = False
        out.write("\n]")

    print("✅ Listo, datos filtrados de la categoria: ", cat)
