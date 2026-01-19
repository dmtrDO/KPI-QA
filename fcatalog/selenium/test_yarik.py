from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time



def setup(ch):
    if (ch==1):
        driver = webdriver.Chrome()
        driver.get("https://librwebapp.pythonanywhere.com/")
    elif (ch==2):
        driver = webdriver.Chrome()
        driver.get("https://librwebapp.pythonanywhere.com/login/")
    else:
        driver = None
    return driver


def tierdown(driver):
    if driver is not None:
        driver.quit()


# def test0():        # тестовий тест
#     setnum = 1
#     driver = setup(setnum)
#     if driver is None:
#         print("Can't find setup choice \'"+str(setnum)+"\'")
#         return False
#     time.sleep(3)

#     tierdown(driver)
#     return True


def find_test():        # тест 1
    setnum = 1
    driver = setup(setnum)
    if driver is None:
        print("Can't find setup choice \'"+str(setnum)+"\'")
        return False
    time.sleep(2)

    submit_b = driver.find_element(by=By.ID, value="input_search")
    submit_b.send_keys("new disc")
    time.sleep(2)

    search_b = driver.find_element(by=By.XPATH, value="//button[@id='search']")
    search_b.click()
    time.sleep(2)

    login_b = driver.find_element(by=By.TAG_NAME, value="a")
    login_b.click()
    time.sleep(2)

    tierdown(driver)
    return True


def assert_test():      # test 2
    setnum = 1
    driver = setup(setnum)
    if driver is None:
        print("Can't find setup choice \'"+str(setnum)+"\'")
        return False

    title = driver.title
    assert title=="Головна"
    time.sleep(2)

    tierdown(driver)
    setnum = 2
    driver = setup(setnum)
    if driver is None:
        print("Can't find setup choice \'"+str(setnum)+"\'")
        return False

    assert "login" in driver.current_url
    time.sleep(2)
    
    tierdown(driver)
    return True


def wait_test():
    setnum = 1
    driver = setup(setnum)
    if driver is None:
        print("Can't find setup choice \'"+str(setnum)+"\'")
        return False
    
    download_b = driver.find_element(by=By.CLASS_NAME, value="download")
    wait = WebDriverWait(driver, timeout=2)
    wait.until(lambda _: download_b.is_displayed())

    tierdown(driver)
    return True


def main():
    # res = test0()
    # if res==True:
    #     print("Тест 0 завершився успішно")
    # else:
    #     print("Тест 0 завершився не успішно!")
    
    res = find_test()
    if res==True:
        print("Тест 1 завершився успішно")
    else:
        print("Тест 1 завершився не успішно!")
    
    res = assert_test()
    if res==True:
        print("Тест 2 завершився успішно")
    else:
        print("Тест 2 завершився не успішно!")
    
    res = wait_test()
    if res==True:
        print("Тест 3 завершився успішно")
    else:
        print("Тест 3 завершився не успішно!")


if __name__=="__main__":
    main()


# кнопка завантажити на головній "<button type="submit" class="download">Завантажити</button>"
# new disc