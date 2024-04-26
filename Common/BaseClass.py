import os
import pytest
import allure
from dotenv import load_dotenv
from pytest_check import check
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


def check_with_screenshot(driver, cond, message):
    with check, allure.step(message):
        if not cond:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="screenshot",
                attachment_type=allure.attachment_type.PNG
            )
        assert cond


class BaseClass:
    load_dotenv()
    url = os.getenv("URL")
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    browsers = os.getenv("BROWSERS")
    browsers = browsers.split(", ")

    @pytest.fixture(scope="class")
    def driver(self, request):
        print(os.getenv("CURRENT_ENV"))
        browser = request.param

        project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if browser == "Edge":
            driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))

            '''edge_driver_path = os.path.join(project_folder, 'Resources', 'msedgedriver')
            serv = EdgeService(edge_driver_path)
            driver = webdriver.Edge(service=serv)'''
        else:
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

            '''chrome_driver_path = os.path.join(project_folder, 'Resources', 'chromedriver')
            serv = ChromeService(chrome_driver_path)
            driver = webdriver.Chrome(service=serv)'''
        driver.implicitly_wait(10)
        driver.maximize_window()
        yield driver
        driver.quit()
