import time
from datetime import datetime

import pytest
from selenium import webdriver

import tools
from config.drivers import get_driver
from config.options import get_options
from constants import OUTPUT_ROOT

BROWSER_NAME = ''


@pytest.fixture(scope="function", autouse=True)
def driver(request):
    options = get_options(BROWSER_NAME)
    driver = get_driver(browser_name=BROWSER_NAME, driver=webdriver, options=options)
    driver.maximize_window()
    driver.implicitly_wait(10)
    request.cls.driver = driver
    yield request.cls.driver
    request.cls.driver.quit()


def pytest_configure(config):
    global BROWSER_NAME
    BROWSER_NAME = config.getoption("--browser")


@pytest.hookimpl
def pytest_addoption(parser):
    parser.addoption('--browser', action='store', default="chrome", help="Choose browser: chrome")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope="function", autouse=True)
def test_failed_check(request):
    yield
    if request.node.rep_setup.failed:
        print("setting up a test failed!", request.node.originalname)
    elif request.node.rep_setup.passed:
        if request.node.rep_call.failed:
            driver = request.cls.driver
            take_screenshot(driver, request.node.originalname)
            print("executing test failed", request.node.originalname)


def take_screenshot(driver, originalname):
    time.sleep(1)
    file_name = \
        f'{originalname}_{datetime.today().strftime("%Y-%m-%d_%H:%M")}.png'.replace("/", "_").replace("::", "__")
    driver.save_screenshot(f"{OUTPUT_ROOT}/{file_name}")


def pytest_collection_modifyitems():
    tools.remove_test_dir(OUTPUT_ROOT)
