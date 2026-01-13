import pytest
import requests
from selenium import webdriver

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#  UI Fixtures (Selenium)
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------

def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chrome", help="browser selection"
    )

@pytest.fixture(scope="function")
def browserInstance(request):
    browser_name = request.config.getoption("--browser_name")

    if browser_name == "chrome":
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        driver= webdriver.Chrome(options=chrome_options)
    elif browser_name == "firefox":
        driver = webdriver.Firefox()


    driver.implicitly_wait(5)
    driver.get("http://localhost:5173/")
    driver.maximize_window()
    yield driver
    driver.quit()



# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#  API Fixtures (requests)
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------

BASE_URL = "http://localhost:5001"

@pytest.fixture(scope="session")
def base_url():
    return BASE_URL

@pytest.fixture(scope="session")
def api_session():
    #Reusable requests session for API calls
    return requests.Session()

@pytest.fixture(scope="session")
def auth_session(base_url, api_session):
    #Authenticate using OTP and return session
    # Step 1: Request OTP
    requestOtp = api_session.post(f"{base_url}/api/auth/request-otp", json={"phone_number": "+256700000000"})
    assert requestOtp.status_code == 200
    # Step 2: Verify OTP (hardcoded to 0000)
    verifyOtp = api_session.post(f"{base_url}/api/auth/verify-otp", json={"phone_number": "+256700000000", "otp": "0000"})
    assert verifyOtp.status_code == 200
    token = verifyOtp.json().get("session_token")
    assert token, "session_token missing in response"
    api_session.headers.update({"Authorization": f"Bearer {token}"})
    return api_session



