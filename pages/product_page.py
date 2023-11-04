import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from base.base_page import BasePage
from base.links import Links
from pages.main_page import MainPage


class ProductPage(BasePage):
    # Locators
    PRODUCT_NAME_LOC = '//h1'
    MANUFACTURER_NAME_LOC = '//table[@class="table table-condensed"]/tbody/tr[1]/td/a'
    BRAND_NAME_LOC = '//table[@class="table table-condensed"]/tbody/tr[2]/td/a'
    COUNTRY_NAME_LOC = '//table[@class="table table-condensed"]/tbody/tr[3]/td/a'
    COLOR_NAME_LOC = '//table[@class="table table-condensed"]/tbody/tr[4]//input[@class="package-color"]'
    PRICE_LOC = '//div[@class="panel-body text-center"]/div/span'
    ACTION_SIGN_LOC = '//div[@class="element-actions alert alert-warning mb-0 mt-20"]/div'
    ACTION_TEXT = "Этот товар участвует в акци"
    ADD_TO_CART_BTN_LOC = '//a[@class="add-element-to-basket btn btn-primary"]'

    #
    # Getters
    #
    def get_product_name(self):
        return self.wait.until(EC.visibility_of_element_located((By.XPATH, self.PRODUCT_NAME_LOC))).text

    def get_product_id(self):
        element = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.ADD_TO_CART_BTN_LOC)))
        product_id = element.get_attribute("data-element-id")
        return product_id

    def get_manufacturer_name(self):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, self.MANUFACTURER_NAME_LOC))).text

    def get_brand_name(self):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, self.BRAND_NAME_LOC))).text

    def get_country_name(self):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, self.COUNTRY_NAME_LOC))).text

    def get_action_flag(self):
        action_text = self.wait.until(EC.visibility_of_element_located((By.XPATH, self.ACTION_SIGN_LOC))).text
        if self.ACTION_TEXT in action_text:
            return True
        else:
            return False

    def get_price(self):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, self.PRICE_LOC))).text    def get_product_data(self, product_id):

        product = []

        # проверяем, что находимся на странице нужного товара
        get_url = self.driver.current_url
        expected_url = f"{Links.CATALOG_PAGE}i{product_id}/"
        assert get_url == expected_url

        product['product_id'] = product_id

        product['name'] = self.wait.until(EC.element_to_be_clickable
                                          ((By.XPATH, self.PRODUCT_NAME_LOC))).text

        product['manufacturer'] = self.wait.until(EC.element_to_be_clickable
                                                  ((By.XPATH, self.PRODUCT_PAGE_MANUFACTURER_NAME_LOC))).text

        product['brand'] = self.wait.until(EC.element_to_be_clickable
                                                  ((By.XPATH, self.BRAND_NAME_LOC))).text

        # product['is_special_price'] = product_special_price_flag

        product['country'] = self.wait.until(EC.element_to_be_clickable
                                             ((By.XPATH, self.PRODUCT_PAGE_COUNTRY_NAME_LOC))).text
        # print(product)
        return product



    #
    # Actions
    #

    #
    # Methods
    #
    # get_product_data(376866)
