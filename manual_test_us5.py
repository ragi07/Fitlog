# Manueller Test für US5: ruft jede Prüffunktion einmal auf
# Ich gebe absichtlich zuerst falsche Werte ein, dann einen richtigen

# Lädt meine Datei validation.py, damit ich die Funktionen benutzen kann
import validation

# Überschrift, damit ich sehe, welcher Test läuft
print("Test 1: Menü (erlaubt 0-10)")
# Ruft die Menüabfrage auf und zeigt das Ergebnis
print("Ergebnis:", validation.read_menu_choice())

# Überschrift für den Gewichtstest
print("Test 2: Gewicht (erlaubt Zahl ab 0)")
# Ruft die Gewichtsabfrage aus und zeigt das Ergebnis an
print("Ergebnis:", validation.read_weight("Weight in kg: "))

# Überschrift für den Datumstest
print("Test 3: Datum (YYYY-MM-DD, leer = heute)")
# Ruft die Datumgsabfrage aus und zeigt das Ergebnis an
print("Ergebnis:", validation.read_date("Date: "))

# Überschrift für den Ja/Nein-Test
print("Test 4: Ja/Nein (y oder n)")
#Ruft die Ja/Nein-Abfrage auf und zeigt das Ergebnis an
print("Ergebnis:", validation.read_yes_no("Continue? (y/n): "))
