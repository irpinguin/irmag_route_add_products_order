import datetime
from colorama import init, Fore, Style
from selenium.webdriver.support.ui import WebDriverWait
from base.data import Data


class BaseClass:

    TIMEOUT = Data.TIMEOUT

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, self.TIMEOUT, poll_frequency=1)

    # Method create screenshot
    def screenshot_make(self):
        # возвращает имя скриншота
        now_date = datetime.datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_name = 'screenshot ' + now_date + '.png'
        self.driver.save_screenshot('./screen/' + screenshot_name)
        return screenshot_name

    # Method measure time
    def get_time_page_load(self, start_time_sec:float, end_time_sec:float, timeout_sec:int = 3):
        # Выводит разницу во времени в секундах и если она меньше таймаута, то выводит ее красным шрифтом
        elapsed_time = end_time_sec - start_time_sec
        if elapsed_time < timeout_sec:
            print(f'\tThe webpage load time: {end_time_sec - start_time_sec:.2f} sec.')
        else:
            print(f'\t{Fore.RED}The webpage load time: {end_time_sec - start_time_sec:.2f} sec '
                  f'is longer than the expected timeout {timeout_sec} sec{Style.RESET_ALL}.')
        return elapsed_time
