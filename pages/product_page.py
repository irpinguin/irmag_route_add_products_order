from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException

from base.base_page import BasePage
from base.links import Links


class ProductPage(BasePage):

    PAGE_URL = Links.CATALOG_PAGE

    # Locators
    PRODUCT_NAME_LOC = '//h1'
    TABLE_LOC = '//table[@class="table table-condensed"]'
    MANUFACTURER_NAME_LOC = f'{TABLE_LOC}/tbody/tr[1]/td/a'
    BRAND_NAME_LOC = f'{TABLE_LOC}/tbody/tr[2]/td/a'
    COUNTRY_NAME_LOC = f'{TABLE_LOC}/tbody/tr[3]/td/a'
    COLOR_NAME_LOC = f'{TABLE_LOC}/tbody/tr[4]//input[@class="package-color"]'
    ACTION_SIGN_LOC = '//div[@class="element-actions alert alert-warning mb-0 mt-20"]/div'
    ACTION_TEXT = "Этот товар участвует в акци"
    PRICE_LOC = '//div[@class="panel-body text-center"]/div/span'
    ADD_TO_CART_BTN_LOC = '//a[@class="add-element-to-basket btn btn-primary"]'

    def __init__(self, driver, product_id):
        super().__init__(driver)
        self.product_id = product_id
        self.driver.get(f"{self.PAGE_URL}i{product_id}")

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
        # элемент присутствует на странице товара только если товар участвует в акции и у него есть спеццена
        try:
            action_text = self.driver.find_element(By.XPATH, self.ACTION_SIGN_LOC).text
            if self.ACTION_TEXT in action_text:
                return True
        except NoSuchElementException:
            return False

    def get_color(self):
        return self.wait.until(EC.visibility_of_element_located((By.XPATH, self.COLOR_NAME_LOC))).accessible_name

    def get_price(self):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, self.PRICE_LOC))).text

    #
    # Actions
    #
    def collect_product_properties(self, product_id):

        product = {}

        # проверяем, что находимся на странице нужного товара
        get_url = self.driver.current_url
        expected_url = f"{Links.CATALOG_PAGE}i{product_id}/"
        # print(get_url, expected_url)
        assert get_url == expected_url

        # получаем данные о свойствах товара
        product['product_id'] = self.get_product_id()
        product['name'] = self.get_product_name()
        product['manufacturer'] = self.get_manufacturer_name()
        product['brand'] = self.get_brand_name()
        product['is_special_price'] = self.get_action_flag()
        product['country'] = self.get_country_name()
        product['color'] = self.get_color()
        product['price'] = self.get_price()

        return product
    #
    # Methods
    #
    # get_product_data(376866)
