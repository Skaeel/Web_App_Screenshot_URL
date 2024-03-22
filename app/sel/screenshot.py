from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


se_event_bus_host = os.getenv('SE_EVENT_BUS_HOST')


def make_screenshot(url: str) -> bytes:
    """
    Создает скриншот веб-страницы с помощью Selenium WebDriver.

    Эта функция настраивает Selenium WebDriver для работы в режиме безголового браузера,
    отключает автоматизированные возможности браузера и подключается к Selenium Event Bus.
    Затем она переходит по указанному URL, ждет загрузки страницы и делает скриншот.
    После этого она закрывает браузер и возвращает скриншот в виде байтов.

    Args:
        url (str): URL веб-страницы, для которой необходимо создать скриншот.

    Returns:
        bytes: Скриншот веб-страницы в формате PNG, представленный в виде байтов.
    """
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Remote(
        command_executor=f'http://{se_event_bus_host}:4444/wd/hub',
        options=options
    )

    driver.get(url)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body')))
        img = driver.get_screenshot_as_png()
    finally:
        driver.quit()
    return img
