import json
import os
import sys
import pytest
from pathlib import Path

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pageObjects.login import LoginPhoneNumber
from pageObjects.loanDetails import Loan_Details  # import Loan_Details

# Dynamically resolve path to test_loanApp.json
test_data_path = Path(__file__).resolve().parent.parent / "data" / "test_loanApp.json"
with open(test_data_path) as f:
    test_data = json.load(f)
    test_list = test_data["data"]

@pytest.mark.parametrize("test_value", test_list)
def test_first_time_loan(browserInstance, test_value):
    driver = browserInstance

    # Login and OTP flow
    login_Page = LoginPhoneNumber(driver)
    verify_otp = login_Page.enter_phone_number(test_value['userPhone'])
    personal_details = verify_otp.otp_request(test_value['otpRequest'])
    personal_details.enter_personal_details(
        test_value['userNames'],
        test_value['userNational_id'],
        test_value['userBirth_date']
    )
    loan_details = personal_details.next_screen_loan_details()

    # Loan details entry
    loan_amount = int(test_value['userLoan_Amount'])
    loan_details.enter_loan_details(
        loan_amount,
        test_value['userLoan_Term'],
        test_value['userLoan_purpose']
    )
    application_summary = loan_details.submit_loan_application(amount=loan_amount)

    if loan_amount >= 1000000:
        pending_msg = application_summary.pending_loan_message()
        print(pending_msg)
    else:
        congratulatoryMessage = application_summary.get_congratulation_message()
        print(congratulatoryMessage)



