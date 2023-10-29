import pytest
from pages.main_page import MainPage
from pages.catalog_page import CatalogPage
from pages.product_page import ProductPage


class BaseTest:

    main_page: MainPage
    catalog_page: CatalogPage
    product_page: ProductPage

    @pytest.fixture(autouse=True)
    def setup(self, request, get_browser_chrome):
        request.cls.driver = get_browser_chrome
        request.cls.main_page = MainPage(get_browser_chrome)
        request.cls.catalog_page = CatalogPage(get_browser_chrome)
        request.cls.product_page = ProductPage(get_browser_chrome)