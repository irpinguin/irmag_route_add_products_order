import pytest
from pages.main_page import MainPage
from pages.catalog_page import CatalogPage


class BaseTest:

    main_page: MainPage
    catalog_page: CatalogPage

    @pytest.fixture(autouse=True)
    def setup(self, request, get_browser_chrome):
        request.cls.driver = get_browser_chrome
        request.cls.main_page = MainPage(get_browser_chrome)
        request.cls.catalog_page = CatalogPage(get_browser_chrome)