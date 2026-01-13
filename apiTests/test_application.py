import json
import pytest
from pathlib import Path
# Dynamically resolve path to test_loanApp.json

test_data_path = Path(__file__).resolve().parent.parent / "apiData" / "test_apiData.json"
with open(test_data_path) as f:
    test_data = json.load(f)
    test_list = test_data["data"]

@pytest.mark.parametrize("test_value",test_list)
def test_submit_application_success(base_url, auth_session,test_value):
    payload = {
        "full_name": test_value['full_name'],
        "national_id": test_value['national_id'],
        "email": test_value['email'],
        "date_of_birth": test_value['date_of_birth'],
        "loan_amount": test_value['loan_amount'],
        "loan_term": test_value['loan_term'],
        "purpose": test_value['purpose']
    }
    successfulApp = auth_session.post(f"{base_url}/api/application/submit", json=payload)
    assert successfulApp.status_code in (200, 201)
    body = successfulApp.json()
    assert body.get("message") == "Application submitted successfully"
    assert "application" in body

@pytest.mark.parametrize("test_value",test_list)
def test_submit_application_invalid(base_url, auth_session,test_value):
    payload = {
        "full_name": "J",  # too short
        "national_id": "CM",  # too short
        "loan_amount": 50,  # too low
        "loan_term": 2,  # invalid term
        "purpose": ""
    }
    invalidApp = auth_session.post(f"{base_url}/api/application/submit", json=payload)
    assert invalidApp.status_code == 400
    body = invalidApp.json()
    assert "errors" in body

@pytest.mark.parametrize("test_value",test_list,)
def test_application_status_no_auth(base_url, api_session,test_value):
    noAuth = api_session.get(f"{base_url}/api/application/status")
    assert noAuth.status_code in (401, 403, 404)

@pytest.mark.parametrize("test_value",test_list)
def test_application_status_with_auth(base_url, auth_session,test_value):
    successAuth = auth_session.get(f"{base_url}/api/application/status")
    assert successAuth.status_code == 200
    body = successAuth.json()
    assert "has_application" in body