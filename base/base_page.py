from selenium.common.exceptions import WebDriverException
from base.base_class import BaseClass


class BasePage(BaseClass):

    def page_open(self):
        try:
            self.driver.get(self.PAGE_URL)
        except WebDriverException:
            print(f"\tОшибка при открытии страницы {self.PAGE_URL}.")
            print(f"\tСоздан скриншот {self.screenshot_make()}.")
            exit(1)

    def assert_page_url(self):
        get_url = self.driver.current_url
        try:
            assert get_url == self.PAGE_URL
            print(f"\tThe current url matches the expected {self.PAGE_URL}.")
        except AssertionError:
            print(f"\tThe current url not matches the expected {self.PAGE_URL}.")

    # Method assert page sign
    def assert_sign(self, text, sign, sample):
        sign_value = sign.text
        print(f"\t{text}", end='')
        try:
            assert sample in sign_value
            print(": OK", end='')
            print(f" (The specified sign '{sample}' is found in '{sign_value}' on the page {self.PAGE_URL}).")
        except AssertionError:
            print(": NOT", end='')
            print(f" (The specified sign '{sample}' is not found in '{sign_value}' on the page {self.PAGE_URL}).")

