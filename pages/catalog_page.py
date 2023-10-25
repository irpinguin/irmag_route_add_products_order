import random
import re
import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait

from base.links import Links
from pages.main_page import MainPage


class CatalogPage(MainPage):

    PAGE_URL = Links.CATALOG_PAGE
    BRANDS_SAMPLE_QTY = 100

    # Locators
    CATALOG_MENU_LOC = '//a[@id="catalog-btn"]'
    CATALOG_SIGN_LOC = '//section[@class="catalog container"]/div[2]/div[1]/nav/ol/li[2]/span'
    CATALOG_SIGN_VAL = "Каталог"
    FILTER_BTN_LOC = '//section[@class="catalog container"]/div[2]/div[2]/button'
    FILTER_SIGN_LOC = FILTER_BTN_LOC
    FILTER_SIGN_VAL = 'Закрыть фильтр'
    FILTER_APPLY_BTN_LOC = '//button[@class="btn-block btn-success btn do-filter"]'

    FILTER_BRAND_BTN_LOC = '//button[@id="dropdown-filter_manufacturer_and_brands_select"]'
    FILTER_BRAND_SEARCH_FLD_LOC = f'{FILTER_BRAND_BTN_LOC}/following-sibling::div/div/input'
    FILTER_BRAND_SIGN_LOC = FILTER_BRAND_SEARCH_FLD_LOC
    FILTER_BRAND_SIGN_VAL = 'Поиск'
    FILTER_BRAND_UL = '/following-sibling::div/ul[@class="dropdown-menu inner"]'
    FILTER_BRAND_LI = f'{FILTER_BRAND_BTN_LOC}{FILTER_BRAND_UL}/li[@class="lvl-2"]'

    PAGE_PERPAGE_360_LOC = '//div[@id="catalog-content"]/div/div[3]/form/select/option[6]'
    CATALOG_CONTENT_LOC = '//div[@id="catalog-content"]/div[3]'

    #
    # Getters
    #
    def get_catalog_page(self):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, self.CATALOG_MENU_LOC)))

    def get_catalog_page_sign(self):
        return self.wait.until(EC.visibility_of_element_located((By.XPATH, self.CATALOG_SIGN_LOC)))

    def get_filter_btn(self):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, self.FILTER_BTN_LOC)))

    def get_filter_sign(self):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, self.FILTER_SIGN_LOC)))

    def get_filter_apply_btn(self):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, self.FILTER_APPLY_BTN_LOC)))

    def get_filter_brand_btn(self):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, self.FILTER_BRAND_BTN_LOC)))

    def get_filter_brand_search_fld(self):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, self.FILTER_BRAND_SEARCH_FLD_LOC)))

    def get_filter_brand_product_qty(self, brand_name):
        btn = self.get_filter_apply_btn()
        match = re.search(r'\((\d+)\)', btn.text)
        if match:
            product_qty = int(match.group(1))
            if product_qty > 0:
                print(f"\tProducts selected for the brand '{brand_name}': {product_qty}")
            elif product_qty == 0:
                print(f"\tProducts of the brand {brand_name} are not available for sale.")
        else:
            print(
                f"\tFor the brand {brand_name}, the 'Применить' button does not show the number of selected products.")
        return product_qty

    def get_products_perpage(self):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, self.PAGE_PERPAGE_360_LOC)))

    def get_catalog_content(self):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, self.CATALOG_CONTENT_LOC)))
    #
    # Actions
    #
    def open_catalog_page(self):
        self.get_catalog_page().click()
        print("\tOn Catalog page the link to the Catalog page is clicked")

    def set_qty_products_per_page(self):
        # Для упрощения, пока устанавливаем 360 товаров на страницу и смотрим-обрабатываем только первую страницу
        self.get_products_perpage().click()

    def health_check(self):
        self.assert_page_url()
        self.assert_sign("Verifying that the Catalog page is open",
                         self.get_catalog_page_sign(), self.CATALOG_SIGN_VAL)

    def filter_open(self):
        btn = self.get_filter_btn()
        btn_state = btn.get_attribute('aria-pressed')
        # print(f'\tFilter state: {btn_state}')
        if btn_state == "false":
            btn.click()
            print("\tOn Catalog page the open filter button is clicked")
        else:
            print("\tThe filter is already open.")
        btn_state = btn.get_attribute('aria-pressed')
        # print(f'\tFilter state: {btn_state}')
        # self.screenshot_make()
        time.sleep(self.TIMEOUT)
        sign = self.get_filter_sign()
        self.assert_sign("Verifying that the filter is open", sign, self.FILTER_SIGN_VAL)

    def filter_brand_open(self):
        self.get_filter_brand_btn().click()
        print("\tFilter Brand button is clicked.")
        print("\tVerifying that the filter is open: ", end='')
        field = self.get_filter_brand_search_fld()
        if field.get_attribute('placeholder') == self.FILTER_BRAND_SIGN_VAL:
            print("OK")
        else:
            print("NOT")

    def select_random_brand(self):
        locator = f'{self.FILTER_BRAND_LI}[{random.randint(1, self.BRANDS_SAMPLE_QTY + 1)}]/a'
        brand = self.driver.find_element(By.XPATH, locator)
        # brand_id = brand.get_attribute('data-id')
        brand_name = brand.text
        print(f"\tFrom the first {self.BRANDS_SAMPLE_QTY} brands, random brand was choosen: {brand_name}.")
        return brand_name

    def filter_brand_select(self, brand_name):
        locator = f'{self.FILTER_BRAND_LI}/a[text()="{brand_name}"]'
        self.get_filter_brand_search_fld().send_keys(brand_name)
        # time.sleep(self.TIMEOUT)
        element = self.driver.find_element(By.XPATH, locator)
        # time.sleep(self.TIMEOUT)
        element.click()
        print(f"\tBrand filter applied: {brand_name}")

    def filter_brand_apply(self):
        self.get_filter_apply_btn().click()
        print("\tThe 'Применить' button is clicked")

    def filter_brand_check(self, brand_name):
        # Возвращает количество
        assert self.get_filter_brand_btn().text == brand_name


    #
    # Methods
    #
    def filter_brand_route(self):
        self.filter_brand_open()
        brand_name = self.select_random_brand()
        self.filter_brand_select(brand_name)
        # time.sleep(self.TIMEOUT/2)
        filtered_product_qty = self.get_filter_brand_product_qty(brand_name)
        self.filter_brand_apply()
        self.filter_brand_check(brand_name)
        self.set_qty_products_per_page()


