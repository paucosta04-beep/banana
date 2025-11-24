# banana# Final Project - Proyecto individual (adaptado a estilo de clase)

Estructura:
- `src/final_project/` : código del simulador (Place, Host, City)
- `main.py` : ejecuta la simulación (v0 y v1) y genera `reports/graph1.png`, `graph2_v0.png`, `graph2_v1.png`
- `notebooks/part2.py` : script con análisis de datos (usar en Jupyter)
- `data/` : poner aquí los CSV descargados de InsideAirbnb (p.ej. `bcn_listings.csv.gz`)
- `reports/` : carpeta donde se guardan los gráficos

Ejecución:
1. Instala dependencias:
   `pip install pandas matplotlib seaborn`
2. Coloca datasets en `data/` (p. ej. `bcn_listings.csv.gz`)
3. Ejecuta `python main.py`
4. Para Part 2, abrir `notebooks/part2.py` en Jupyter y ejecutar celdas.

Seed: `12345` (reproducible).