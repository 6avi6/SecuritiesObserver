from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


# Inicjalizacja opcji przeglądarki Chrome
options = Options()
options.add_argument("--start-maximized")  # Otwórz okno przeglądarki w maksymalnym rozmiarze

# Inicjalizacja serwisu i przeglądarki Chrome
driver_service = Service(ChromeDriverManager().install())
driver_service.start()
driver = webdriver.Chrome(service=driver_service, options=options)

# Adres strony, na której chcesz zczytać ciasteczka
url = "https://stooq.pl"

# Otwarcie strony w przeglądarce
driver.get(url)

# Poczekaj na załadowanie strony i interakcję użytkownika, aby zaakceptować ciasteczka
time.sleep(3)  # Poczekaj 10 sekund na ręczne zaakceptowanie ciasteczek
button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'fc-cta-consent')))
button.click()
 # Poczekaj 10 sekund na przekierowanie na nową stronę
time.sleep(3) 
# Zczytanie ciasteczek
cookies = driver.get_cookies()

cookies_data = {}
for cookie in cookies:
    cookies_data[cookie['name']] = cookie['value']

# Zapisanie ciasteczek do pliku cookies.py
with open('cookie.py', 'w') as f:
    f.write("cookies = {\n")
    for name, value in cookies_data.items():
        f.write(f"    \"{name}\":\"{value}\",\n")
    f.write("}\n")

# Zakończenie działania przeglądarki
driver.quit()
