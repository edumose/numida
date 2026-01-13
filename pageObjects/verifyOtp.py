from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pageObjects.personalDetails import PersonalDetails


class VerifyOtp:
    def __init__(self, driver):
        self.driver = driver
        self.oneTimePassword = (By.CSS_SELECTOR, "input[id*='otp']")
        self.blankField = (By.XPATH, "(//button[text()='Verify'])[1]")
        self.enterOTP = (By.XPATH, "(//button[text()='Verify'])[1]")

    def otp_request(self, OTP):
        # Verify OTP
        wait = WebDriverWait(self.driver, 10)

        # Step 1: Locate OTP input
        otp_input = wait.until(EC.presence_of_element_located(self.oneTimePassword))

        # Step 2: Click Verify without entering OTP
        verify_button = wait.until(EC.element_to_be_clickable(self.blankField))
        verify_button.click()

        # Step 3: Check validity
        is_valid = self.driver.execute_script("return arguments[0].checkValidity();", otp_input)

        if not is_valid:
            print("Validation triggered: OTP field is empty.")

            # Step 4: Enter OTP
            otp_input.send_keys(OTP)

            # Step 5: Re-check validity after entering OTP
            is_valid_after = self.driver.execute_script("return arguments[0].checkValidity();", otp_input)
            print("OTP field valid after entry?", is_valid_after)

            # Step 6: Click Verify again
            verify_button = wait.until(EC.element_to_be_clickable(self.enterOTP))
            verify_button.click()
            personal_details = PersonalDetails(self.driver)
            return personal_details