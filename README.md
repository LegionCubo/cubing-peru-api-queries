# 🇵🇪 Cubing Perú QUERIES - Procesamiento de Datos WCA

Este proyecto contiene scripts en **Python** que procesan los archivos exportados de la **World Cube Association (WCA)** para generar datos filtrados de competiciones, personas, resultados de Perú.

---

## ⚡ Requisitos

- Instalar dependencias necesarias:
  - py -m pip install ijson
  - py -m pip install requests

## Orden de ejecucion de queries

- El proceso es sencillo simplemente en tu local ejecutas py name_del_archivo.py
1. descargar_wca.py (Demora aprox 10 minutos)
2. query_wca_results_peru.py (Demora aprox 30 segundos)
3. query_wca_results_peru_for_cat.py
4. query_wca_competitions_peru.py
5. query_wca_persons_peru.py
5. query_wca_persons_delegates_peru.py
5. query_wca_persons_organisers_peru.py

- Antes que nada creas las carpetas padres 
1. crea la carpeta salida_json
2. crea la carpeta cubing-peru-api-v0 al costado de esta carpeta de queries
cubing-peru-api-v0/
├── Persons/
│   └── Delegates/
│   └── Organisers/
├── Competitions/
│   └── 
├── Organisers/
│   └── 
├── Results/
│   └── 