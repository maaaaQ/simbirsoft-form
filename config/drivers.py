from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


def get_driver(browser_name: str, driver, options):
    if browser_name == 'chrome':
        return driver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    if browser_name == 'firefox':
        return driver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
