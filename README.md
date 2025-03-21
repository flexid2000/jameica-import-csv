# jameica-import-csv

Python script to import Postbank CSV Table into Hibiscus/Jameica

## Usage

1. Install `python3-pandas`
2. Export transaction table as csv on Postbank website
3. Adjust present `Kontostand` in `convert-to-hibiscus.py`
4. `python convert-to-hibiscus.py umsaetze.csv` -> `hibiscus_import.csv`
5. In Jameica, go to `Start` > `Hibiscus` > `Konten`: choose aktive account
6. Right click > `Umsätze importieren` > `CSV-Format`: choose `hibiscus_import.csv`
7. Adjust columns
8. Done
