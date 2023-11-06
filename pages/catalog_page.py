import random
import re
import time
from tqdm import tqdm

from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from base.links import Links
from base.base_page import BasePage


from pages.product_page import ProductPage


class CatalogPage(BasePage):

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
    FILTER_USAGE_SIGN_LOC = '//div[@class="alert alert-success"]'
    # FILTER_CLEAR_LOC = '//a[@class="btn btn-danger btn-xs"]'

    FILTER_BRAND_BTN_LOC = '//button[@id="dropdown-filter_manufacturer_and_brands_select"]'
    FILTER_BRAND_SEARCH_FLD_LOC = f'{FILTER_BRAND_BTN_LOC}/following-sibling::div/div/input'
    FILTER_BRAND_SIGN_LOC = FILTER_BRAND_SEARCH_FLD_LOC
    FILTER_BRAND_SIGN_VAL = 'Поиск'
    FILTER_BRAND_UL = '/following-sibling::div/ul[@class="dropdown-menu inner"]'
    FILTER_BRAND_LI = f'{FILTER_BRAND_BTN_LOC}{FILTER_BRAND_UL}/li[@class="lvl-2"]'
    FILTER_BRAND_CLEAR_LOC = '//a[@class="reset-selected pull-right"]'

    PAGE_PER_PAGE_360_LOC = '//div[@id="catalog-content"]/div/div[3]/form/select/option[6]'

    CATALOG_ITEM_LOC = '//div[@id="catalog-content"]/div[3]/div'
    CATALOG_ITEM_PRODUCT_ID_2_LOC = '/div/div[3]/div/a'
    CATALOG_ITEM_PRODUCT_NAME_2_LOC = '/div/div[2]/a'
    CATALOG_ITEM_PRODUCT_PRICE_SPEC_LOC = '//span[@class="price"]'
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

    def get_filter_brand_clear(self):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, self.FILTER_BRAND_CLEAR_LOC)))

    def get_filter_brand_btn(self):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, self.FILTER_BRAND_BTN_LOC)))

    def get_filter_brand_search_fld(self):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, self.FILTER_BRAND_SEARCH_FLD_LOC)))

    def get_filter_brand_btn_text(self):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, self.FILTER_BRAND_BTN_LOC))).text

    def get_filter_brand_product_qty(self, brand_name):
        btn = self.get_filter_apply_btn()
        match = re.search(r'\((\d+)\)', btn.text)
        if match:
            product_qty = int(match.group(1))
            if product_qty > 0:
                print(f"\t- Number of products selected for the brand '{brand_name}': {product_qty}")
            elif product_qty == 0:
                print(f"\t- Products of the brand {brand_name} are not available for sale.")
        else:
            product_qty = None
            print(f"\t- For the brand {brand_name}, the 'Применить' button does not show the number "
                  f"of selected products.")
        return product_qty

    def get_products_per_page(self):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, self.PAGE_PER_PAGE_360_LOC)))

    def get_filter_state(self):
        btn = self.get_filter_btn()
        btn_state = btn.get_attribute('aria-pressed')
        if btn_state == "false":
            return False
        return True

    def get_filter_usage_state(self):
        try:
            self.driver.find_element(By.XPATH, self.FILTER_USAGE_SIGN_LOC)
            return True
        except NoSuchElementException:
            print("Filter usage sign not found")
            return False

    def get_catalog_item_special_price_flag(self, catalog_item_element, catalog_item_locator):
        # получаем признак наличия специальной цены
        try:
            catalog_item_element.find_element(By.XPATH, catalog_item_locator)
            return True
        except NoSuchElementException:
            return False

    #
    # Actions
    #
    def open_catalog_page(self):
        self.get_catalog_page().click()
        print("\tOn Catalog page the link to the Catalog page is clicked")

    def set_qty_products_per_page(self):
        # Для упрощения, пока устанавливаем 360 товаров на страницу и смотрим-обрабатываем только первую страницу
        self.get_products_per_page().click()

    def filter_open(self):
        filter_state = self.get_filter_state()
        if filter_state:
            print("\tThe filter is already open.")
        else:
            self.get_filter_btn().click()
            print("\tOn Catalog page the open filter button is clicked.")
        # TODO: разобраться с ожиданием: после того как кликнули почему то надо дать время прогрузиться?
        time.sleep(self.TIMEOUT)
        sign = self.get_filter_sign()
        self.assert_sign("Verifying that the filter is open", sign, self.FILTER_SIGN_VAL)

    def filter_brand_reset(self):
        # сбрасывается фильтр по бренду, но заголовок "Используется фильтрация" остается
        if self.get_filter_brand_btn_text():
            self.get_filter_brand_clear().click()
        print("The filter Brand has been reset.")

    def filter_reset(self):
        # TODO: спросить, что делать в случаях, когда сталкиваемся с перехватчиком (может это влияние таймаута?)
        # на странице действует перехватчик, поэтому элемент '//a[@class="btn btn-danger btn-xs"]' не кликабелен
        # element click intercepted: Element <a href="/cat/" class="btn btn-danger btn-xs">...</a> is not
        # clickable at point (317, 63). Other element would receive the click:
        # <div class="block-2 col-xs-12 col-sm-8 col-sm-push-1 col-md-8 col-md-push-2 pt-15 pb-15">...</div>
        # Сейчас сброс фильтра через переоткрытие страницы по новой, что собственно и сделано по локатору

        filter_state = self.get_filter_usage_state()
        if filter_state:
            self.driver.get(self.PAGE_URL)
        print("The filter has been reset.")

    def filter_brand_open(self):
        self.get_filter_brand_btn().click()
        print("\tFilter Brand button is clicked.")

        # assert
        print("\t- Verifying that the filter Brand is open: ", end='')
        assert self.get_filter_brand_search_fld().get_attribute('placeholder') == self.FILTER_BRAND_SIGN_VAL
        print("OK.")

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
        element = self.driver.find_element(By.XPATH, locator)
        element.click()
        print(f"\tBrand filter applied: {brand_name}.")

    def filter_brand_apply(self):
        self.get_filter_apply_btn().click()
        print("\tThe 'Применить' button is clicked.")

    def collect_catalog_content_items(self):

        products = []

        catalog_items = self.driver.find_elements(By.XPATH, self.CATALOG_ITEM_LOC)

        # для каждого элемента каталога
        for i in range(len(catalog_items)):
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
            locator = f'{self.CATALOG_ITEM_LOC}[{i + 1}]{self.CATALOG_ITEM_PRODUCT_SPECIAL_PRICE_SIGN_LOC}'
            product_special_price_flag = self.get_catalog_item_special_price_flag(catalog_items[i], locator)
            product['is_special_price'] = product_special_price_flag

            # получаем цену, если есть специальная цена, то данные по цене находятся по другому XPath
            if product_special_price_flag:
                locator = f'{self.CATALOG_ITEM_LOC}[{i + 1}]{self.CATALOG_ITEM_PRODUCT_PRICE_SPEC_LOC}'
            else:
                locator = f'{self.CATALOG_ITEM_LOC}[{i + 1}]{self.CATALOG_ITEM_PRODUCT_ID_2_LOC}'
            product_price = catalog_items[i].find_element(By.XPATH, locator)
            product['price'] = product_price.text

            products.append(product)

        return products

    def collect_catalog_content_items_data_from_product(self, products):
        i = 0
        products_from_product_pages = []
        progress_bar = tqdm(products,
                            desc='\tCollecting data from product pages',
                            unit='product',
                            ncols=80)
        for product in progress_bar:
            product_page = ProductPage(self.driver, product['product_id'])
            product_data = product_page.collect_product_properties(product['product_id'])
            products_from_product_pages.append(product_data)
            self.driver.back()

        return products_from_product_pages

    def set_sorting_novelty(self):
        pass

    def set_sorting_popularity(self):
        pass

    #
    # Methods
    #
    def health_check(self):
        print("Verifying that the Catalog page is opened correctly.")
        self.assert_page_url()
        self.assert_sign("Verifying that the Catalog page is open",
                         self.get_catalog_page_sign(), self.CATALOG_SIGN_VAL)

    def filter_brand_route(self):
        print("Verify that the brand filter in the catalog is working correctly.")
        self.filter_brand_open()
        # TODO убрать фиксированный бренд
        # brand_name = self.select_random_brand()
        brand_name = "Old Spice"
        self.filter_brand_select(brand_name)
        # после выбора бренда и до применения фильтра на кнопке "Применить" отображается количество товаров в фильтре
        # после того, как фильтр применили, количество товаров на кнопке "Применить" уже не отображается
        filter_brand_product_qty = self.get_filter_brand_product_qty(brand_name)
        self.filter_brand_apply()
        self.set_qty_products_per_page()

        # self.get_catalog_content_items()
        assert self.get_filter_brand_btn().text == brand_name
        print(f"\t- The button displays the name of the expected brand: {brand_name}.")

        catalog_content_items = self.collect_catalog_content_items()
        # print(f'\ncatalog_content_items:\n{catalog_content_items}\n')

        # в содержании каталога есть не вся информация о товаре, поэтому
        # для каждого представленного товара ходим на страницу товара и там получаем полные данные
        print("\tGet data about each product from the product page:")
        catalog_content_items_data_from_product = self.collect_catalog_content_items_data_from_product(catalog_content_items)

        # print(f'\ncatalog_content_items_data_from_product:\n{catalog_content_items_data_from_product}\n')

        # проверяем, что количество отобранных товаров совпадает со значением, которое было на кнопке "Применить"
        catalog_content_items_qty = len(catalog_content_items)
        assert filter_brand_product_qty == catalog_content_items_qty
        print(f"\t- The number of products selected in the brand filter: {filter_brand_product_qty} "
              f"is the same as the number of products in the catalog content: {catalog_content_items_qty}.")

        # проверяем, что в содержимом отфильтрованного каталога нет товаров других брендов
        for product in catalog_content_items_data_from_product:
            assert product['brand'] == brand_name
        print(f'\t- In the content of the filtered catalog, there are only products of the selected brand: {brand_name}')

        # проверяем, что количество товаров со спецценой одинаковое на странице товаров и по данным со страниц товаров
        catalog_content_items_with_special_price = 0
        catalog_content_items_data_from_product_with_special_price = 0

        for product in catalog_content_items:
            if product['is_special_price']:
                catalog_content_items_with_special_price += 1
        for product in catalog_content_items_data_from_product:
            if product['is_special_price']:
                catalog_content_items_data_from_product_with_special_price += 1
        assert catalog_content_items_with_special_price == catalog_content_items_data_from_product_with_special_price
        print(f"\t- The number of products with a special price is the same on the product page: "
              f"{catalog_content_items_with_special_price} and according to the data from the product pages: "
              f"{catalog_content_items_data_from_product_with_special_price}")

        # проверяем, что цены для товаров одинаковы на странице каталога и на странице продукта
        diff = []
        for catalog_content_product, product_from_page in zip(
                catalog_content_items, catalog_content_items_data_from_product):
            if catalog_content_product['price'] != product_from_page['price']:
                diff.append(f"Difference in price for the product {catalog_content_product['name']}: "
                            f"{catalog_content_product['price']} != {product_from_page['price']}")
        assert not diff, f"The following price differences were found:\n{', '.join(diff)}"
        print("\t- For all items in the filtered catalog, the price is the same as the price on the product page.")
