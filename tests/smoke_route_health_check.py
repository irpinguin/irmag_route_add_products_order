import pytest
import requests
from base.links import Links


class TestRouteProductOrder:

    @pytest.mark.smoke
    @pytest.mark.parametrize("url",
        [Links.MAIN_PAGE, Links.LOGIN_PAGE, Links.REGISTER_PAGE, Links.CATALOG_PAGE, Links.CATALOG_SUBCAT_PAGE]
        )
    def test_health_check(self, url):
        response = requests.session().get(url.strip())          # Делаем запрос по указанному url
        assert response.status_code == 200                      # Проверяем успешную загрузку страницы
        assert response.url.startswith("https://")              # Проверяем использование HTTPS
        assert response.elapsed.total_seconds() < 5             # Проверяем время ответа на запрос
