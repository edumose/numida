from selenium.webdriver.common.by import By

from pageObjects.loanDetails import Loan_Details


class PersonalDetails:
    def __init__(self, driver):
        self.driver = driver
        self.customerName = (By.ID, "fullName")
        self.idNumber = (By.ID, "nationalId")
        self.dateOfBirth = (By.XPATH, "//input[@id='dob']")
        self.nextButton = (By.CSS_SELECTOR, "button[type='submit']")




    def enter_personal_details(self,Full_names, National_Id, Dob):
        #Enter personal details of customer
        self.driver.find_element(*self.customerName).send_keys(Full_names)
        self.driver.find_element(*self.idNumber).send_keys(National_Id)
        self.driver.find_element(*self.dateOfBirth).send_keys(Dob)



    #Clicking the next screen to go to loan details page
    def next_screen_loan_details(self):
        self.driver.find_element(*self.nextButton).click()
        loan_details = Loan_Details(self.driver)
        return loan_details

