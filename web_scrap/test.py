from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import webbrowser

# env
driver_path = 'C:/Users/spvis/Downloads/geckodriver-v0.33.0-win64/geckodriver.exe'
brave_path = 'C:/Program Files/Mozilla Firefox/firefox.exe'

# initalize
# User agent to mimic a real browser (you can change this)
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Set up ChromeOptions with additional options
options = webdriver.FirefoxOptions()
options.binary_location = brave_path

# Add user agent and other headers
options.add_argument(f'user-agent={user_agent}')
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-impl-side-painting")
options.add_argument("--disable-setuid-sandbox")
options.add_argument("--disable-seccomp-filter-sandbox")
options.add_argument("--disable-breakpad")
options.add_argument("--no-sandbox")
driver = webdriver.Firefox(executable_path=driver_path, options=options)

# URL of the website you want to scrape
url = 'https://main.sci.gov.in/judgments'

# Load the webpage
driver.get(url)

time.sleep(2)
# driver.implicitly_wait(3)
# Find the dropdown element and select "Judgment Date"
# dropdown = Select(driver.find_element_by_id('tabbed-nav'))
# dropdown.select_by_visible_text('Judgment Date')
driver.find_element_by_link_text("Judgment Date").click()

# Find the <p> tag with id='cap'
cap_paragraph = driver.find_element_by_id('cap')

# Find the <font> tag within the <p> tag
font_tag = cap_paragraph.find_element_by_tag_name('font')

# Extract the text from the <font> tag
font_text = font_tag.text

# Find the input element with id='ansCaptcha'
captcha_input = driver.find_element_by_id('ansCaptcha')

# Enter the extracted font_text into the input element
captcha_input.send_keys(font_text)

# Explicitly wait for the submit button to become clickable
# wait = WebDriverWait(driver, 10)
# submit_button = wait.until(EC.element_to_be_clickable((By.ID, 'v_getJBJ')))

# Click the submit button
# submit_button.click()

# Wait for the page to load completely
driver.implicitly_wait(3)  # You may need to adjust the wait time


# Enter the "From Date" and "To Date" using user input
from_date = input("Enter 'From Date' (DD-MM-YYYY): ")
to_date = input("Enter 'To Date' (DD-MM-YYYY): ")

from_date_input = driver.find_element(By.ID, 'JBJfrom_date')
from_date_input.clear()
from_date_input.send_keys(from_date)

to_date_input = driver.find_element(By.ID, 'JBJto_date')
to_date_input.clear()
to_date_input.send_keys(to_date)

# Find the "Submit" button with id='v_getJBJ' and click it
submit_button = driver.find_element(By.ID, 'v_getJBJ')
submit_button.click()

# Wait for new data to load
time.sleep(5)  # You may need to adjust the time depending on the page load time

# Get the page source after clicking the "Submit" button
page_source = driver.page_source

# Use BeautifulSoup to parse the page source
soup = BeautifulSoup(page_source, 'html.parser')

# Find the <div> with id='JBJ' and extract the table
jbj_div = soup.find('div', {'id': 'JBJ'})
table = jbj_div.find('table')

# Save the table as an HTML file
with open('table.html', 'w', encoding='utf-8') as file:
    file.write(table.prettify())


webbrowser.open('table.html')

# Close the browser
driver.quit()

# Print the extracted value
print(f"Text inside <font>: {font_text}")
