from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from base.links import Links
from base.base_page import BasePage


class MainPage(BasePage):

    PAGE_URL = Links.MAIN_PAGE

    # Locators
    MAIN_PAGE_SIGN_LOC = '//div[@id="index-last-blog-posts"]/h2'
    MAIN_PAGE_SIGN_VAL = 'Новые обзоры в блоге'
    CATALOG_MENU_LOC = '//a[@id="catalog-btn"]'

    # Getters
    def get_main_page_sign(self):
        return self.wait.until(EC.visibility_of_element_located((By.XPATH, self.MAIN_PAGE_SIGN_LOC)))

    def get_catalog_menu(self):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, self.CATALOG_MENU_LOC)))

    # Actions
    def open_catalog_page(self):
        self.get_catalog_menu().click()
        print("\tOn Main page the link to the Catalog page is clicked")

    # Methods
    def health_check(self):
        self.assert_page_url()
        self.assert_sign("Verifying that the Main page is open",
                         self.get_main_page_sign(), self.MAIN_PAGE_SIGN_VAL)