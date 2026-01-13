from selenium.webdriver.common.by import By




from selenium.webdriver.common.by import By

from pageObjects.verifyOtp import VerifyOtp


class LoginPhoneNumber:
    def __init__(self, driver):
        self.driver = driver
        self.phoneNumber = (By.ID, "phone")
        self.submitButton = (By.CSS_SELECTOR, "button[type='submit']")
        self.startApp = (By.XPATH, "//button[text()='Start Application']")

    # Enter phone number page
    def enter_phone_number(self, disNumber):
        self.driver.find_element(*self.startApp).click()
        self.driver.find_element(*self.phoneNumber).send_keys(disNumber)
        self.driver.find_element(*self.submitButton).click()
        message = self.driver.find_element(By.CSS_SELECTOR, "div[class='step-container'] p").text
        assert "Enter the OTP sent to" in message
        verify_otp = VerifyOtp(self.driver)
        return verify_otp






