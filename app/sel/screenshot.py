from selenium import webdriver
import os


def make_screenshot(url: str) -> bytes:
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Remote(
        command_executor='http://selenium-hub:4444/wd/hub',
        options=options
    )

    driver.get(url)
    driver.implicitly_wait(10)
    img = driver.get_screenshot_as_png()
    driver.quit()
    return img


def save_screenshot(img_data: bytes, path: str) -> None:
    with open(path, 'wb') as file:
        file.write(img_data)


def delete_screenshot(path: str) -> None:
    os.remove(path)
