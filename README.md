# 🇵🇪 Cubing Perú QUERIES - Procesamiento de Datos WCA

Este proyecto contiene scripts en **Python** que procesan los archivos exportados de la **World Cube Association (WCA)** para generar datos filtrados de competiciones, personas, resultados de Perú.

---

## ⚡ Requisitos

- Instalar dependencias necesarias:
  - py -m pip install ijson
  - py -m pip install requests

## Orden de ejecucion de queries

- El proceso es sencillo simplemente en tu local ejecutas py name_del_archivo.py
1. descargar_wca.py (Demora aprox 10 minutos) | Descarga el archivo de la wca
2. query_wca_results_peru.py (Demora aprox 30 segundos) | descarga los resultados de peru
3. query_wca_persons_peru.py | Separa las personas de Peru
4. query_wca_competitions_peru.py | Separa las competiciones que fueron organizadas o delegadas y participadas por peruanos
5. query_wca_results_peru_single_for_cat.py | Separa los resultados y los ordena de menor a mayor por categoria (single)
6. query_wca_results_peru_average_for_cat.py | Separa los resultados y los ordena de menor a mayor por categoria (average)
7. query_wca_rank_peru.py | Obtenemos los rankings de cada categoria
8. query_wca_rank_sum_single_peru.py | Ranking de sumatoria por single
9. query_wca_rank_sum_average_peru.py | Ranking de sumatoria por average
10. query_wca_persons_peru_segundo_paso.py | edita el archivo de personas añadiendo ultima competencia y podios
11. query_wca_persons_delegates_peru.py | Separa los delegados
12. query_wca_persons_organisers_peru.py | Separa los organizadores

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