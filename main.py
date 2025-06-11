
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import json
import os

def init_browser():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=options)

def login_to_site(driver):
    driver.get("https://bc78999.net")
    time.sleep(3)

    # 輸入帳號與密碼
    driver.find_element(By.ID, "username").send_keys("32048")
    driver.find_element(By.ID, "password").send_keys("000")

    # 點擊登入按鈕
    driver.find_element(By.CLASS_NAME, "login-btn").click()
    time.sleep(5)

    # 點擊「真人」 > 「DG真人」
    driver.find_element(By.PARTIAL_LINK_TEXT, "真人").click()
    time.sleep(2)
    driver.find_element(By.PARTIAL_LINK_TEXT, "DG真人").click()
    time.sleep(10)  # 等待 DG 載入

def parse_table_info(driver):
    tables = []
    elements = driver.find_elements(By.CLASS_NAME, "table-item")  # 根據實際 class 名稱調整

    for el in elements[:5]:  # 只抓前5桌做展示
        try:
            table_no = el.find_element(By.CLASS_NAME, "table-id").text
            dealer = el.find_element(By.CLASS_NAME, "dealer-name").text
            players = el.find_element(By.CLASS_NAME, "online-count").text

            tables.append({
                "桌號": table_no,
                "荷官": dealer,
                "在線人數": players
            })
        except:
            continue

    return tables

def save_tables(tables):
    with open("output/tables.json", "w", encoding="utf-8") as f:
        json.dump(tables, f, ensure_ascii=False, indent=2)

def main():
    driver = init_browser()
    try:
        login_to_site(driver)
        tables = parse_table_info(driver)
        save_tables(tables)
    except Exception as e:
        print("錯誤：", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
