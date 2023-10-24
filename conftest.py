# Причина, по которой в pycharm runner может  не передается фикстура
# https://intellij-support.jetbrains.com/hc/en-us/community/posts/12897247432338-PyCharm-unable-to-find-fixtures-in-conftest-py
#
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


@pytest.fixture(autouse=True, scope="function")
def get_browser(request):
    service = Service(executable_path='./utilities/chromedriver-116.0.5845.96.exe')
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--window-size=1920,1080")
    options.add_experimental_option("detach", True)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service=service, options=options)
    request.cls.driver = driver
    yield driver
    # driver.quit()