from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Запуск Firefox
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
driver.get("https://librwebapp.pythonanywhere.com/")

try:
    # === ТЕСТ 1: Локатори (пункт а) ===
    # 1. Локатор ID (поле вводу)
    driver.find_element(By.ID, "input_search").send_keys("Асинхронність")

    time.sleep(2)

    # 2. Локатор XPath (обов'язково) - кнопка пошуку
    driver.find_element(By.XPATH, "//button[@id='search']").click()

    time.sleep(2)

    # 3. Локатор CSS Selector - посилання на логін
    login_link = driver.find_element(By.CSS_SELECTOR, "div.login a")

    print("Test 1 OK: Елементи знайдено трьома способами.")

    # === ТЕСТ 2: Очікування (пункт в) ===
    login_link.click()

    # Explicit Wait: чекаємо 5 сек, поки з'явиться заголовок "Авторизація"
    wait = WebDriverWait(driver, 5)
    auth_label = wait.until(EC.visibility_of_element_located((By.ID, "text_auth")))

    print("Test 2 OK: Очікування спрацювало, сторінка завантажилась.")

    # === ТЕСТ 3: Перевірки/Asserts (пункт б) ===
    # Перевірка 1: Заголовок вкладки
    assert driver.title == "Login", "Помилка Title"

    time.sleep(1)

    # Перевірка 2: URL адреса
    assert "login" in driver.current_url, "Помилка URL"

    time.sleep(1)

    # Перевірка 3: Текст на сторінці
    assert auth_label.text == "Авторизація", "Помилка тексту"

    print("Test 3 OK: Всі перевірки пройшли успішно.")

except Exception as e:
    print(f"Помилка: {e}")
finally:
    driver.quit()
