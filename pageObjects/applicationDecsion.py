from selenium.webdriver.common.by import By


class Application_Decision:
    def __init__(self,driver):
        self.driver = driver
        self.decisionMessage = (By.XPATH, "(//p[@class='decision-message'])[1]")
        self.containerMessage = (By.CSS_SELECTOR,
            "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(3)")
        self.logoutPage = (By.XPATH, "(//button[normalize-space()='Logout'])[1]")


    def get_congratulation_message(self):
        congratulatoryMessage = self.driver.find_element(*self.decisionMessage).text
        assert "Congratulations!" in congratulatoryMessage
        return congratulatoryMessage


    def get_decision_summary_card_items(self):

        # Locate the parent container (the div that holds all summary items)
        parent_container = self.driver.find_element(*self.containerMessage)
        # Finding all child divs inside that container
        child_divs = parent_container.find_elements(By.TAG_NAME, "div")
        # Loop through each child div and print its text
        for index, div in enumerate(child_divs, start=1):
            print(f"{index}: {div.text.strip()}")


    def logout(self):
        self.driver.find_element().click()