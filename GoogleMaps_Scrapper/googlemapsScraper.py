from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import quote
import time
import os
import pandas as pd

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)



keyword = "coffee shop in Jakarta"
url = f"https://www.google.com/maps/search/{quote(keyword)}"
driver.get(url)

time.sleep(7)

# cari panel hasil sebelah kiri
scrollable_div = driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')

# scroll beberapa kali supaya lebih banyak bisnis ke-load
for i in range(10):
    driver.execute_script(
        "arguments[0].scrollTop = arguments[0].scrollHeight",
        scrollable_div
    )
    time.sleep(2)

business_cards = driver.find_elements(By.CLASS_NAME, "hfpxzc")

data = []

for card in business_cards:
    name = card.get_attribute("aria-label")
    link = card.get_attribute("href")

    if name and link:
        data.append({
            "Keyword": "coffee shop",
            "Location": "Jakarta",
            "Business Name": name,
            "Google Maps URL": link
            })

df = pd.DataFrame(data)

# hapus duplicate
df = df.drop_duplicates()

os.makedirs("data", exist_ok=True)
df.to_csv("data/google_maps_leads.csv", index=False)

print(df)
print(f"Total data: {len(df)}")
print("Data berhasil disimpan!")