# jameica-import-csv

Python script to import Postbank CSV Table into Hibiscus/Jameica

## Usage

1. Export transaction table as csv on Postbank website
2. Adjust present `Kontostand` in `convert-to-hibiscus.py`
3. `python convert-to-hibiscus umsaetze.py umsaetze.csv` -> `hibiscus_import.csv`
4. In Jameica, go to `Start` > `Hibiscus` > `Konten`: choose aktive account
5. Right click > `Umsätze importieren` > `CSV-Format`: choose `hibiscus_import.csv`
6. done
