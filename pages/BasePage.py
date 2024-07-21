from selenium.common import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException

class BasePage:
    TIME = 15

    def __init__(self, driver):
        self.driver = driver

    def _get_attribute(self, element: tuple, attribute: str):
        return self.driver.find_element(*element).get_attribute(attribute)

    def _wait_and_click(self, element: tuple):
        WebDriverWait(self.driver, ignored_exceptions=(NoSuchElementException, StaleElementReferenceException),
                      timeout=self.TIME) \
            .until(EC.element_to_be_clickable(element)) \
            .click()

    def _click(self, element: tuple):
        wait = WebDriverWait(self.driver, timeout=10)
        try:
            el = wait.until(EC.element_to_be_clickable(element))
            el.click()
        except ElementClickInterceptedException:
            print("Trying to click on the button again")
            self.driver.execute_script("arguments[0].click()", el)

    def _find_element(self, element: tuple):
        return self.driver.find_element(*element)

    def _wait_element(self, element: tuple):
        try:
            return WebDriverWait(self.driver, self.TIME).until(EC.presence_of_element_located(element))
        except TimeoutException and NoSuchElementException:
            msg = f'Element not found, element: "{element}"'
            raise NoSuchElementException(msg)

    def _elements_presenter(self, element: tuple) -> bool:
        return bool(len(self.driver.find_elements(*element)))

    def _clear_field(self, element: tuple):
        self.driver.find_element(*element).clear()

    def _go_to_url(self, url: str) -> None:
        self.driver.get(url)

    def _fill_field(self, element: tuple, text: str):
        el = self._wait_element(element)
        el.send_keys(text)

    def _press_key(self, element: tuple, keys):
        self.driver.find_element(element).send_keys(keys)

    def _get_text(self, element: tuple):
        return self._wait_element(element).text

    def _element_visible(self, element: tuple):
        try:
            element = self.driver.find_element(*element)
            return element.is_displayed()
        except NoSuchElementException:
            return False
