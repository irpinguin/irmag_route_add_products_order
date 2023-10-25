import pytest
from base.base_test import BaseTest


class TestRouteProductOrder(BaseTest):

    # @pytest.mark.smoke
    def test_route_product_order(self):
        print("\n")
        # print("Open the main page.")
        # self.main_page.page_open()
        # self.main_page.health_check()

        print("Go to the catalog page.")
        # self.main_page.open_catalog_page()
        self.catalog_page.page_open()
        self.catalog_page.health_check()
        self.catalog_page.filter_open()
        self.catalog_page.filter_brand_route()
