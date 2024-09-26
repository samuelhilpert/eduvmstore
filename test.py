# Dieser Kommentar überschreitet absichtlich die maximale Zeilenlänge von 88 Zeichen, um die Zeilenlängenregel zu testen.
import os, sys  # Unbenutzte Importe und falsche Importreihenfolge

def BADLY_named_function():  # Falsche Namenskonvention für Funktionen (sollte snake_case sein)
    print("Hallo, Welt!")

def main():
    print("Dies ist ein Test für Ruff.")  # Der Code funktioniert, aber enthält Linting-Fehler
    if True: print("Syntax-Fehler hier!")  # Syntaxfehler (fehlendes Doppelpunkt)

if __name__ == "__main__":
    main()
