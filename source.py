import csv
import openpyxl
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

def generatecrc32(text):
    url = "https://emn178.github.io/online-tools/crc32.html"
    driver.get(url)
    input_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'input')))
    input_field.clear()
    input_field.send_keys(text)
    driver.find_element(By.ID, 'execute').click()
    return WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'output'))).get_attribute('value')

#Nolasa vārdus un ģenerē CRC32 kodus
names_crc32 = {}
with open("people.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        full_name = f"{row['First Name']} {row['Last Name']}"
        names_crc32[full_name] = generatecrc32(full_name)

driver.quit()

#Algu identifikācija
salaries = {}
wb = openpyxl.load_workbook('salary.xlsx')
sheet = wb.active
for row in sheet.iter_rows(min_row=2, values_only=True):
    for name, crc32_code in names_crc32.items():
        if crc32_code == row[0]:
            salaries[name] = salaries.get(name, 0) + row[1]

#Rezultātu izvade
for name, salary in salaries.items():
    print(f"Darbinieks: {name}, Alga: {salary}")
