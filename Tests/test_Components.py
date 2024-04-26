import time
import pytest
import random
import allure
from pytest_check import check
from selenium.webdriver.common.by import By
from Common.BaseClass import BaseClass
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys


@pytest.mark.parametrize("driver", ["Chrome"], indirect=True)
class TestComponents(BaseClass):

    def test_1(self, driver):
        driver.get("https://demo.automationtesting.in/Slider.html")
        driver.find_element(By.XPATH, "//button[@aria-label='Do not consent']").click()
        slider = driver.find_element(By.ID, "slider")
        slider_button = driver.find_element(By.XPATH, "//div[@id='slider']/a")
        desired_position = random.randint(1, 99)
        print(desired_position)

        slider_width = slider.size['width']
        slider_height = slider.size['height']
        print(slider_width)
        print(slider_height)

        offset = slider_width * desired_position / 100
        print(offset)

        action = ActionChains(driver)
        action.click_and_hold(slider_button).move_by_offset(offset, 0).release().perform()

        time.sleep(5)

        style = slider_button.get_attribute("style")
        with check, allure.step("Mouse slide"):
            assert style == f"left: {desired_position}%;"

        with check, allure.step("Keystroke down arrow"):
            ActionChains(driver).key_up(Keys.ARROW_DOWN).key_down(Keys.ARROW_DOWN).perform()
            desired_position = desired_position - 1
            style = slider_button.get_attribute("style")
            assert style == f"left: {desired_position}%;"

        with check, allure.step("Keystroke up arrow"):
            ActionChains(driver).key_up(Keys.ARROW_UP).key_down(Keys.ARROW_UP).perform()
            desired_position = desired_position + 1
            style = slider_button.get_attribute("style")
            assert style == f"left: {desired_position}%;"

    def test_2(self, driver):
        driver.get("https://demo.automationtesting.in/Alerts.html")
        driver.find_element(By.XPATH, "//a[@href='#OKTab']").click()
        driver.find_element(By.XPATH, "//button[@class='btn btn-danger']").click()
        alert = Alert(driver)
        with check, allure.step("Regular alert"):
            assert alert.text == "I am an alert box!"
        alert.accept()

        driver.find_element(By.XPATH, "//a[@href='#CancelTab']").click()
        driver.find_element(By.XPATH, "//button[@class='btn btn-primary']").click()
        alert = Alert(driver)
        with check, allure.step("Optional alert text"):
            assert alert.text == "Press a Button !"
        alert.accept()
        with check, allure.step("Optional alert after accepting"):
            assert driver.find_element(By.ID, "demo").text == "You pressed Ok"
        driver.find_element(By.XPATH, "//button[@class='btn btn-primary']").click()
        alert = Alert(driver)
        alert.dismiss()
        with check, allure.step("Optional alert after declining"):
            assert driver.find_element(By.ID, "demo").text == "You Pressed Cancel"

        username = 'simple user'
        driver.find_element(By.XPATH, "//a[@href='#Textbox']").click()
        driver.find_element(By.XPATH, "//button[@class='btn btn-info']").click()
        alert = Alert(driver)
        with check, allure.step("Alert with text box"):
            assert alert.text == "Please enter your name"
        alert.send_keys(username)
        alert.accept()
        with check, allure.step("Accept alert with text box"):
            assert driver.find_element(By.ID, "demo1").text == f"Hello {username} How are you today"
        driver.find_element(By.XPATH, "//button[@class='btn btn-info']").click()
        alert = Alert(driver)
        alert.send_keys(username)
        alert.dismiss()
        with check, allure.step("Dismiss alert with text box"):
            assert driver.find_element(By.ID, "demo1").text == ""
