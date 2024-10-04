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
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions


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
    email = os.getenv("EMAIL")
    email_password = os.getenv("EMAIL_PASSWORD")
    browsers = browsers.split(", ")

    @pytest.fixture(scope="class")
    def driver(self, request):
        browser = request.param

        project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        is_ci = os.getenv('CI') == 'true'
        if is_ci:
            if browser == "Edge":
                # Set up Edge options
                options = EdgeOptions()
                options.add_argument("--headless")
                options.add_argument("--disable-gpu")
                options.add_argument("--window-size=1920,1080")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-extensions")
                options.add_argument("--disable-infobars")
                serv = EdgeService(EdgeChromiumDriverManager().install())
                driver = webdriver.Edge(service=serv, options=options)
            else:
                options = ChromeOptions()
                options.add_argument("--headless")
                options.add_argument("--disable-gpu")
                options.add_argument("--window-size=1920,1080")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-extensions")
                options.add_argument("--disable-infobars")
                '''chrome_driver_path = "/usr/local/share/chrome_driver/chromedriver"
                serv = ChromeService(executable_path=chrome_driver_path)
                driver = webdriver.Chrome(service=serv, options=options)'''
                chrome_driver_path = "/usr/bin/chromedriver"
                serv = ChromeService(chrome_driver_path)
                driver = webdriver.Chrome(service=serv, options=options)
        else:
            if browser == "Edge":
                edge_driver_path = os.path.join(project_folder, 'Resources', 'msedgedriver')
                serv = EdgeService(edge_driver_path)
                driver = webdriver.Edge(service=serv)
            else:
                chrome_driver_path = os.path.join(project_folder, 'Resources', 'chromedriver')
                serv = ChromeService(chrome_driver_path)
                driver = webdriver.Chrome(service=serv)
        driver.implicitly_wait(10)
        driver.maximize_window()
        yield driver
        driver.quit()

    '''@pytest.fixture(scope="session", autouse=True)
    def setup_project_directory(self, request):
        project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        reports_path = os.path.join(project_folder, 'Reports')
        reports_history_path = os.path.join(reports_path, 'history')
        allure_history_path = os.path.join(project_folder, 'allure-report', 'history')

        # Clear the content of the Reports directory
        for item in os.listdir(reports_path):
            item_path = os.path.join(reports_path, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)

        # Create Reports/history directory if it doesn't exist
        #os.makedirs(reports_history_path, exist_ok=True)

        # Copy contents of allure-history into Reports/history
        shutil.copytree(allure_history_path, reports_history_path)

        # Teardown: Execute a terminal command at the end of the session
        def generate_report():
            # Replace "your_command" with the terminal command you want to execute
            command = "allure generate ./Reports --clean"
            subprocess.run(command, shell=True, check=True)

        request.addfinalizer(generate_report)'''
