import random
import re
import time

from selenium.common import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
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

    PAGE_PER_PAGE_360_LOC = '//div[@id="catalog-content"]/div/div[3]/form/select/option[6]'

    CATALOG_ITEM_LOC = '//div[@id="catalog-content"]/div[3]/div'
    # CATALOG_ITEM_PRODUCT_ID_1_LOC = f'{CATALOG_ITEM_LOC}'
    CATALOG_ITEM_PRODUCT_ID_2_LOC = '/div/div[3]/div/a'
    # CATALOG_ITEM_PRODUCT_NAME_1_LOC = f'{CATALOG_ITEM_LOC}'
    CATALOG_ITEM_PRODUCT_NAME_2_LOC = '/div/div[2]/a'
    CATALOG_ITEM_PRODUCT_PRICE_LOC = f'{CATALOG_ITEM_PRODUCT_NAME_2_LOC}//span[@class="price"]'
    CATALOG_ITEM_PRODUCT_SPECIAL_PRICE_SIGN_LOC = '//i[@class="prop-special-price fa fa-fw"]'

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
                print(f"\tNumber of products selected for the brand '{brand_name}': {product_qty}")
            elif product_qty == 0:
                print(f"\tProducts of the brand {brand_name} are not available for sale.")
        else:
            print(
                f"\tFor the brand {brand_name}, the 'Применить' button does not show the number of selected products.")
        return product_qty

    def get_products_per_page(self):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, self.PAGE_PER_PAGE_360_LOC)))

    # def get_catalog_content(self):
    #     # возвращает список элементов
    #     elements = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.CATALOG_CONTENT_LOC)))
    #     return elements

    # def get_product_special_price_sign(self, locator):
    #     return self.wait.until(EC.element_to_be_clickable((By.XPATH, locator)))

    #
    # Actions
    #
    def open_catalog_page(self):
        self.get_catalog_page().click()
        print("\tOn Catalog page the link to the Catalog page is clicked")

    def set_qty_products_per_page(self):
        # Для упрощения, пока устанавливаем 360 товаров на страницу и смотрим-обрабатываем только первую страницу
        self.get_products_per_page().click()

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
        print(f"\tFrom the first {self.BRANDS_SAMPLE_QTY} brands, random brand was chosen: {brand_name}.")
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

        # TODO: проверить, что на отфильтрованной странице верное количество товаров
        #   проверить, что все товары принадлежат выбранному бренду,
        #   список полученных товаров как-то сохранить для дальнейшего применения

        catalog_items = self.driver.find_elements(By.XPATH, self.CATALOG_ITEM_LOC)
        catalog_items_qty = len(catalog_items)
        print(f'catalog_items_qty= {catalog_items_qty}')
        products = []

        # для каждого элемента каталога
        for i in range(catalog_items_qty):
            product = {}

            # получаем product_id
            locator = f'{self.CATALOG_ITEM_LOC}[{i + 1}]{self.CATALOG_ITEM_PRODUCT_ID_2_LOC}'
            product_id = catalog_items[i].find_element(By.XPATH, locator).get_attribute("data-element-id")
            product['product_id'] = product_id

            # получаем Наименование товара
            locator = f'{self.CATALOG_ITEM_LOC}[{i + 1}]{self.CATALOG_ITEM_PRODUCT_NAME_2_LOC}'
            product_name = catalog_items[i].find_element(By.XPATH, locator)
            product['name'] = product_name.text

            # получаем признак наличия специальной цены
            # если есть специальная цена, то данные по цене находятся по другому XPath
            locator = f'{self.CATALOG_ITEM_LOC}[{i + 1}]{self.CATALOG_ITEM_PRODUCT_SPECIAL_PRICE_SIGN_LOC}'
            try:
                catalog_items[i].find_element(By.XPATH, locator)
                product_special_price_flag = True
            except NoSuchElementException:
                product_special_price_flag = False
            product['is_special_price'] = product_special_price_flag

            # почему-то этот код выдергивает цену, если товар акционный, то обе цены
            # и нам надо взять вторую цену, если она есть
            # или заниматься определением акционный товар или нет
            # locator = f'{self.CATALOG_ITEM_PRODUCT_ID_1_LOC}[{i + 1}]{self.CATALOG_ITEM_PRODUCT_PRICE_LOC}'
            # product_price = catalog_items[i].find_element(By.XPATH, locator)
            # product['price'] = product_price.text

            products.append(product)

        # for product in products:
        #     print("Product ID:", product['product_id'])
        #     print("Name:", product['name'])
        #     print("Price:", product['price'])
        #     print()
        print(products)


    #
    # Methods
    #
    def filter_brand_route(self):
        self.filter_brand_open()
        # brand_name = self.select_random_brand()
        brand_name = "Old Spice"
        self.filter_brand_select(brand_name)
        # time.sleep(self.TIMEOUT/2)
        filtered_product_qty = self.get_filter_brand_product_qty(brand_name)
        self.filter_brand_apply()
        self.set_qty_products_per_page()
        self.filter_brand_check(brand_name)
