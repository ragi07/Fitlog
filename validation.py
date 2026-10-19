# Dieser Part enthält die Eingabeprüfungen für Fitlog US5
# Jede Funktion fragt so lange nach, bis die Eingabe gültig ist, damit das Programm nie wegen einer Fehleingabe abstürzt

# Pythons Werkzeug zur Prüfung von Kalenderdaten (heutiges Datum etc.)
import datetime
# Pythons Mathe-Werkzeug
import math

# kleinste erlaubte Menüauswahl (0 = Pogramm beenden)
MENU_MIN = 0
# grösste erlaubte Menüauswahl (Optionen 0 bis 10)
MENU_MAX = 10

# Definiert die Funktion read_int mit drei Parametern: Fragetext, kleinste und grösste erlaubte Zahl:
def read_int(prompt, min_value, max_value):
    
    #Fragt eine ganze Zahl im Bereich min_value bis max_value ab und wiederholt die Frage bei Fehler:
    #Endlosschleife: sie endet erst, wenn unten "return" eine gültige Zahl zurückgibt
    while True: 
        
        #zeigt den Fragetext an und speichert die Eingabe als Text (input liefert immer str).
        text = input(prompt)
        
        # "try" heisst: Versuche die nächste Zeile, klappt sie nicht, geht es bei expect weiter.
        try: 

            #wandelt den Text in eine Zahl um, z.b. "5" -> 5. Bei ABC entsteht ein ValueError
            number = int(text)

            #wird ausgeführt, wenn int() mit einem ValueError gescheitert ist (d.h. keine ganze Zahl)
        except ValueError:

            #Erklärt dem User, was erlaubt ist.
            print("Invalid Input! Please enter a whole number from [min_value] to [max_value].")

            #Springt wieder zurück an den Anfang: die Frage wird wiederholt
            continue

        #Prüft ob die eingegebene Zahl zu klein oder zu gross ist:
        if number < min_value or number >max_value:

            #Gleiche Fehlermeldung wie oben, damit der Benutzer den erlaubten Bereich sieht
            print("Invalid Input! Please enter a whole number from [min_value] to [max_value].")

            #Zurück an den Anfang: nochmals fragen
            continue

        #Hier ist die Zahl gültig: sie wird zurückgegeben und die Schleife endet hier
        return number

#Definiert die Funkltion read_menu_choice ohne Parameter
def read_menu_choice():

    #Fragt die Menüauswahl 0 bis 10 ab: diese Funktion ist für main.py 
    #User read_int mit den Menügrenzen und gibt deren Ergebnis direkt zurück
    return read_int("Choose an option ([MENU_MIN]-[MENU_MAX])")

#Definiert die Funktion read_weight mit dem Fragetext als Parameter
def read_weight(prompt):

    #Fragt ein Gewicht in kg ab: Zahl ab 0, Komma oder Punkt als Dezimaltrennzeichen
    #Endlosschleife: Sie endet erst mit einem gültigen Gewicht
    while True:

        #Liest die Eingabe, entfernt Leerzeichen am Rand (strip) und ersetzt ein Komma durch einen Punkt
        text = input(prompt).strip().replace(",", ".")

        #Versucht Text in Komma umzuwandeln
        try:

            #Wandelt den Text in eine Kommazahl um (von "52.5" zu 52.5)
            weight = float(text)

            #Wird ausgeführt wenn der Text keine Zahl ist (ABC) oder leere Eingabe
        except ValueError:

            #Erklärt welche Eingabe erwartet wird
            print("Invalid weight. Please enter a number of at least 0")

            #Nochmals fragen
            continue

        #isfinite ist False für "inf" (unendlich) und "nan" (keine Zahl): beides keine korrekte Eingabe bzw. kein echtes Gewicht
        if not math.isfinite(weight):

            #Erklärt den Fehler
            print("Invalid weight. The weight must be at least 0 kg.")

            #Nochmals Fragen
            continue

        #Das Gewicht ist gültig und wird zurückgegeben
        return weight

#Definiert die Funktion is_valid_date, die einen Text bekommt und True oder False zurückgibt:
def is_valid_date(text):

        #Prüft ob der Text genau die Form YYYY-MM-DD hat und eine echter Kalendertag ist.
        #Form prüfen: genau 10 Zeichen, an Position 4 und 7 ein Bindestrich (Trennzeichen)
        if len(text) != 10 or text[4] != "-" or text[7] != "-":

            #Falsche Form z.b 19.10.2026
            return False

        #Versuche aus dem Text ein echtes Datum zu machen
        try:

            #Geht nur bei einem echten Tag, 2026.02.30 löst ein ValueError aus:
            datetime.date.fromisoformat(text)

            #Wird ausgeführt, wenn es diesen Tag nicht gibt:
        except ValueError:

            #kein echter Kalendertag:
            return False

        #Form und Tag stimmen:
        return True

#definiert die Funktion read_date mit dem Fragetext als Parameter
def read_date(prompt):

    #Fragt ein Datum ab; eine leere Eingabe bedeutet heute. Zurückgegeben wird der Text YYYY-MM-DD
    #Endlosschleife: sie endet erst mit einem gültigen Datum
    while True:

        #Liest die Eingabe und entfernt Leerzeichen
        text = input(prompt).strip()

        #Leere Eingabe?
        if text == "":

            #Gibt das heute Datum als Text zurück
            return datetime.date.today().isoformat()

        #Ist der Text ein gültiges Datum?
        if is_valid_date(text):

            #Gültiges Datum zurückgeben
            return text

    #Weder leer noch gültig: Fehlermeldung, fragt nochmals
    print("Invalid date. Please use the format YYYY-MM-DD with a real calendar day")

#Definiert die Funktion read_yes_no mit dem Fragetext als Parameter
def read_yes_no(prompt):

    #Fragt eine Ja/Nein Antwort ab und gibt True für y und False für n zurück
    while True:

        #Liest die Eingabe, entfernt Leerzeichen und macht Grossbuchstaben klein
        answer = input(prompt).strip().lower()

        #Antwort y = ja
        if answer == "y":

            #True zurückgeben
            return True

        #Antwort n = nein
        if answer == "n":

            #False zurückgeben
            return False

        #Alles andere ist ungültig, Fehlermeldung, dann fragt nochmals
        print("Invalid answer. Please enter y (yes) or n (no)")






        