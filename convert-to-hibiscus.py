import pandas as pd

# Pfade zur Eingabe- und Ausgabedatei
input_file = 'umsaetze.csv'  # Postbank-CSV
output_file = 'hibiscus_import.csv'  # Hibiscus/Jamaica-kompatible CSV
error_file = 'fehlerhafte_datensaetze.csv'  # Datei für fehlerhafte Datensätze

# Spaltenüberschriften der Postbank-CSV (ab Zeile 8)
postbank_columns = [
    "Buchungstag", "Wert", "Umsatzart", "Begünstigter / Auftraggeber", "Verwendungszweck",
    "IBAN / Kontonummer", "BIC", "Kundenreferenz", "Mandatsreferenz", "Gläubiger ID",
    "Fremde Gebühren", "Betrag", "Abweichender Empfänger", "Anzahl der Aufträge",
    "Anzahl der Schecks", "Soll", "Haben", "Währung"
]

# Spaltenüberschriften der Hibiscus/Jamaica-CSV
hibiscus_columns = [
    "#", "IBAN", "BIC", "Konto", "Gegenkonto", "Gegenkonto BLZ", "Gegenkonto Inhaber",
    "Betrag", "Valuta", "Datum", "Verwendungszweck", "Verwendungszweck 2", "Zwischensumme",
    "Primanota", "Kundenreferenz", "Kategorie", "Notiz", "Weitere Verwendungszwecke",
    "Art", "Vormerkbuchung", "End-to-End ID"
]

# Postbank-CSV einlesen (überspringe die ersten 7 Zeilen und verwende Zeile 8 als Header)
df_postbank = pd.read_csv(input_file, sep=';', skiprows=7, header=0, names=postbank_columns, encoding='latin1')

# Neue DataFrames für Hibiscus/Jamaica und fehlerhafte Datensätze erstellen
df_hibiscus = pd.DataFrame(columns=hibiscus_columns)
df_errors = pd.DataFrame(columns=postbank_columns)  # Für fehlerhafte Datensätze

# Letzter Kontostand vor dem ersten neuen Datensatz (manuell anpassen!)
letzter_kontostand = 1000.00  # Beispielwert, ersetzen Sie dies durch den tatsächlichen Saldo

# Daten zuordnen und auf Fehler prüfen
for index, row in df_postbank.iterrows():
    try:
        # Datum in ein datetime-Objekt umwandeln, um später sortieren zu können
        datum = pd.to_datetime(row["Buchungstag"], format="%d.%m.%Y")

        # Tausendertrennzeichen (Punkte) entfernen und Komma durch Punkt ersetzen
        betrag = row["Betrag"].replace(".", "").replace(",", ".")
        betrag = float(betrag)  # In Fließkommazahl umwandeln

        # Verwendungszweck kürzen (auf 100 Zeichen begrenzen) und Sonderzeichen entfernen
        verwendungszweck = row["Verwendungszweck"][:100].replace("\n", " ").replace(";", " ")

        # Daten zuordnen
        new_row = {
            "#": index + 1,
            "IBAN": row["IBAN / Kontonummer"],
            "BIC": row["BIC"],
            "Konto": "",
            "Gegenkonto": row["IBAN / Kontonummer"],
            "Gegenkonto BLZ": "",
            "Gegenkonto Inhaber": row["Begünstigter / Auftraggeber"],
            "Betrag": betrag,  # Bereinigter Betrag
            "Valuta": row["Wert"],
            "Datum": datum.strftime("%d.%m.%Y"),  # Datum korrekt formatieren
            "Verwendungszweck": verwendungszweck,  # Verwendungszweck kürzen und bereinigen
            "Verwendungszweck 2": "",
            "Primanota": "",
            "Kundenreferenz": row["Kundenreferenz"],
            "Kategorie": "",
            "Notiz": row["Umsatzart"],
            "Weitere Verwendungszwecke": "",
            "Art": "",
            "Vormerkbuchung": "",
            "End-to-End ID": ""
        }
        df_hibiscus = df_hibiscus._append(new_row, ignore_index=True)  # Geändert von append zu _append
    except Exception as e:
        # Fehlerhafte Zeile in die Fehler-DF aufnehmen
        df_errors = df_errors._append(row, ignore_index=True)  # Geändert von append zu _append
        print(f"Fehler in Zeile {index + 8}: {e}")

# Datensätze nach Datum sortieren (aufsteigend)
df_hibiscus = df_hibiscus.sort_values(by="Datum")

# Zwischensumme (Saldo) berechnen
df_hibiscus["Zwischensumme"] = letzter_kontostand + df_hibiscus["Betrag"].cumsum()

# Zwischensumme auf zwei Dezimalstellen runden
df_hibiscus["Zwischensumme"] = df_hibiscus["Zwischensumme"].round(2)

# Ergebnis in eine neue CSV-Datei schreiben
df_hibiscus.to_csv(output_file, sep=';', index=False, encoding='latin1')

# Fehlerhafte Datensätze in eine separate Datei schreiben
if not df_errors.empty:
    df_errors.to_csv(error_file, sep=';', index=False, encoding='latin1')
    print(f"Fehlerhafte Datensätze wurden in {error_file} gespeichert.")

print(f"Die konvertierte Datei wurde erfolgreich gespeichert: {output_file}")