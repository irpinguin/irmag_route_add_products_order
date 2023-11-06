import time

import datetime
from base.base_test import BaseTest
from base.data import Data


class TestRouteProductOrder(BaseTest):

    # @pytest.mark.smoke
    def test_route_product_order(self):
        now_date = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\nStart: {now_date} UTC")
        # print("Open the Main page.")
        # self.main_page.page_open()
        # self.main_page.health_check()

        print("Open the Catalog page.")
        # self.main_page.open_catalog_page()
        self.catalog_page.page_open()
        self.catalog_page.health_check()
        self.catalog_page.filter_open()
        self.catalog_page.filter_brand_route()
        self.catalog_page.filter_brand_reset()
        # self.catalog_page.filter_reset()