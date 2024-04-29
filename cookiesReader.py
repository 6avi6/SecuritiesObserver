from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


# Initialize Chrome browser options
options = Options()
options.add_argument("--start-maximized")  # Open the browser window in maximum size

# Initialize Chrome service and browser
driver_service = Service(ChromeDriverManager().install())
driver_service.start()
driver = webdriver.Chrome(service=driver_service, options=options)

# URL of the page from which you want to read cookies
url = "https://stooq.pl"

# Open the page in the browser
driver.get(url)

# Wait for the page to load and for user interaction to accept cookies
time.sleep(3)  # Wait for 3 seconds for manual cookie acceptance
button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'fc-cta-consent')))
button.click()
# Wait for 3 seconds for redirection to a new page
time.sleep(3)

# Read cookies
cookies = driver.get_cookies()
#write cookies in proper pyton format
cookies_data = {}
for cookie in cookies:
    cookies_data[cookie['name']] = cookie['value']

# Save cookies to a cookies.py file
with open('cookie.py', 'w') as f:
    f.write("cookies = {\n")
    for name, value in cookies_data.items():
        f.write(f"    \"{name}\":\"{value}\",\n")
    f.write("}\n")

# Close the browser
driver.quit()