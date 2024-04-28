from datetime import datetime

def printTime():
    # Pobierz bieżącą datę i czas
    current_time = datetime.now()

    # Pobierz godzinę, minutę i sekundę
    hour = current_time.hour
    minute = current_time.minute
    second = current_time.second

    # Formatuj wynik do postaci "godzina:minuta:sekunda"
    formatted_time = "{:02d}:{:02d}:{:02d}".format(hour, minute, second)

    # Wyświetl bieżącą godzinę, minutę i sekundę
    print("Time", formatted_time)