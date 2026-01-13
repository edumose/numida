import json
import pytest
from pathlib import Path
# Dynamically resolve path to test_loanApp.json

test_data_path = Path(__file__).resolve().parent.parent / "apiData" / "test_apiData.json"
with open(test_data_path) as f:
    test_data = json.load(f)
    test_list = test_data["data"]

@pytest.mark.parametrize("test_value",test_list)
def test_request_success_otp(base_url, api_session, test_value):
    requestingOtp = api_session.post(f"{base_url}/api/auth/request-otp", json={"phone_number": test_value['phone_number']})
    assert requestingOtp.status_code == 200
    body = requestingOtp.json()
    assert body.get("message") == "OTP sent successfully"
    assert body.get("phone_number") == test_value['phone_number']

@pytest.mark.parametrize("test_value",test_list)
def test_request_invalid_otp(base_url, api_session,test_value):
    requestingOtp = api_session.post(f"{base_url}/api/auth/request-otp", json={"phone_number": "070"})
    assert requestingOtp.status_code == 400
    assert "error" in requestingOtp.json()

@pytest.mark.parametrize("test_value",test_list)
def test_verify_success_otp(base_url, api_session,test_value):
    api_session.post(f"{base_url}/api/auth/request-otp", json={"phone_number": test_value['phone_number']})
    verifyingOtp = api_session.post(f"{base_url}/api/auth/verify-otp", json={"phone_number": test_value['phone_number'], "otp": test_value['otp']})
    assert verifyingOtp.status_code == 200
    body = verifyingOtp.json()
    assert body.get("message") == "Authentication successful"
    assert "session_token" in body

@pytest.mark.parametrize("test_value",test_list)
def test_verify_invalid_otp(base_url, api_session,test_value):
    verifyingOtp = api_session.post(f"{base_url}/api/auth/verify-otp", json={"Phone_number": test_value['phone_number'], "otp": test_value['otp']})
    assert verifyingOtp.status_code == 401
    assert "error" in verifyingOtp.json()