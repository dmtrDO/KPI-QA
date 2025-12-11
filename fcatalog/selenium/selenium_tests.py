from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
driver.get("https://librwebapp.pythonanywhere.com/")

try:
    # 1. Локатор ID (поле вводу)
    driver.find_element(By.ID, "input_search").send_keys("Асинхронність")
    time.sleep(2)
    driver.find_element(By.XPATH, "//button[@id='search']").click()
    time.sleep(2)
    login_link = driver.find_element(By.CSS_SELECTOR, "div.login a")
    print("Елементи знайдено")

    login_link.click()

    wait = WebDriverWait(driver, 5)
    auth_label = wait.until(EC.visibility_of_element_located((By.ID, "text_auth")))

    print("Сторінка завантажилась.")

    assert driver.title == "Logind", "Помилка Title"
    time.sleep(1)
    assert "login" in driver.current_url, "Помилка URL"
    time.sleep(1)
    assert auth_label.text == "Авторизація", "Помилка тексту"
    print("Перевірки пройшли успішно.")

except Exception as e:
    print(f"Помилка: {e}")
finally:
    driver.quit()
