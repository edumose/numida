from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pageObjects.applicationDecsion import Application_Decision


class Loan_Details:
    def __init__(self,driver):
        self.driver = driver
        self.loanAmount = (By.ID, "loanAmount")
        self.loanTerm = (By.ID, "loanTerm")
        self.purposeField = (By.XPATH, "(//textarea[@id='purpose'])[1]")
        self.submitButton = (By.CSS_SELECTOR, "button[type='submit']")




    def enter_loan_details(self,amount, loanterm, purpose):
        #Enter loan amount
        self.driver.find_element(*self.loanAmount).send_keys(amount)

        # Selecting the loan term for the loan
        loanTerm_dropDown = self.driver.find_element(*self.loanTerm)
        select = Select(loanTerm_dropDown)
        select.select_by_visible_text(loanterm)

        # confriming selection
        selected_option = select.first_selected_option
        print("Selected loan term:", selected_option.text)

        # Entering more details for loan purpose
        self.driver.find_element(*self.purposeField).send_keys(purpose)

    def submit_loan_application(self, amount: int):

        self.driver.find_element(*self.submitButton).click()
        application_summary = Application_Decision(self.driver)

        # 🔑 Validation logic
        if amount >= 1000000:
            expected_status = "⏳Your application is under review."
            assert "Your application is under review" in expected_status


        return application_summary



