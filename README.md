# Numida QA Test Suite

## Project Overview
This repository contains automated QA tests for the **Numida Loan Application API**.  
The suite validates core functionality across:
- Health check endpoints
- Authentication (OTP request & verification)
- Loan application submission & status

The goal is to ensure **functional correctness, validation enforcement, and security compliance**.

## Tech Stack
- **Language:** Python 3.13
- **Framework:** Pytest 9.0
- **Environment:** Virtualenv (`.venv`)
- **Libraries:** requests, pytest-html, pytest-xdist

## Project Structure
```text
Numida/
├─ .venv/                          # Virtual environment
├─ apiData/                        # Additional API test data
│  └─ test_apiData.json
├─ apiTests/                       # API test suites
│  ├─ test_application.py
│  ├─ test_authentication.py
│  └─ test_healthcheck.py
├─ data/                           # Loan application test data
│  └─ test_loanApp.json
├─ LoanApplication/                # Loan application test logic
│  ├─ __init__.py
│  └─ test_loanApp.py
├─ pageObjects/                    # Page Object Model for UI flows
│  ├─ __init__.py
│  ├─ applicationDecsion.py
│  ├─ loanDetails.py
│  ├─ login.py
│  ├─ personalDetails.py
│  ├─ verifyOtp.py
│  └─ conftest.py
├─ loanApp.py                      # Core loan application logic or helper module
└─ External Libraries / Scratches  # IDE-managed folders

Path handling: Tests load JSON data using pathlib for portability:

python
from pathlib import Path
import json

test_data_path = Path(__file__).resolve().parent.parent / "data" / "test_loanApp.json"
test_list = json.loads(Path(test_data_path).read_text())["data"]

test_data_path = Path(__file__).resolve().parent.parent / "apiData" / "test_apiData.json"
test_list = json.loads(Path(test_data_path).read_text())["data"]


How to run tests
Run all API tests:
bash
pytest apiTests/

Run a specific file:
bash
pytest apiTests/test_application.py

Generate an HTML report:
bash
pytest --html=report.html

How to run tests
Run all LoanApp tests:
bash
pytest LoanApplication/

Run a specific file:
bash
pytest LoanApplication/loanApp.py

Generate an HTML report:
bash
pytest --html=report.html

Application (apiTests/test_application.py)
Total tests: 4
Passed: 1
Failed: 3

Test Plan can be accessed via this link: 

## Architecture And Design Decisions
Overall Test Architecture

## Layered Testing Approach
• Unit Tests: Validate individual validation rules (e.g. application, authentication and Healthcheck api ).
• API/Integration Tests: Verify endpoint behavior, status codes, and session flows.
• End-to-End Scenarios: Cover critical business workflows such as loan application, OTP verification, and duplicate submission handling.
• Automation Framework: Built with Pytest + Requests library for lightweight, maintainable API automation.
• Fixtures: Used for environment setup (e.g., session tokens, test data, parameterization) to ensure reproducibility.

## Test Suite Structure
## Validation Suite
• Covers edge cases (empty fields, invalid formats, oversized payloads, date boundaries).

## Session Suite
• Focuses on session lifecycle, expiry, and mapping to customer phone numbers.

## Error Handling Suite
• Ensures consistent status codes (200, 400, 401, 404, 409) and clear error messages.

## Persistence Suite
• Verifies OTP flows and state consistency across endpoints.

## Regression Suite
• Automates repeatable checks to prevent reintroduction of known defects.

## Design Decisions
• Pytest chosen for readability, fixture management, and scalability.
• Page Object Model (POM) principles applied to keep test flows modular and reusable.
• Separation of Concerns: Suites are isolated by functionality (validation, sessions, error handling) to simplify debugging and reporting.
• Human-readable reporting: HTML reports integrated for stakeholder visibility.

## Trade-offs Considered
## Speed vs Coverage
• Prioritized critical flows (session, OTP, duplicate handling) over exhaustive scenarios due to time constraints.

## Manual vs Automated
• Automated regression for repeatable API checks and UI Happy path flow; manual exploratory testing for edge cases requiring judgment (e.g., session expiry, OTP flows).

## Lightweight Framework vs Enterprise Tools
- Chose Pytest for simplicity and speed of setup, and avoided multiple negative scenarios that would increase a lot of work.

Failure details:
## test_submit_application_success: Expected 200/201, got 400.
• Gap: Valid payload rejected, possibly due to duplicate detection or stricter rules (e.g., future DOB)

## test_submit_application_invalid: Expected “errors” object, got {"error": "Application already exists"}.
• Gap: Validation feedback is missing when duplicates exist.

## test_application_status_no_auth: Expected 401/403/404, got 200 OK.
• Gap: Endpoint accessible without authentication—potential security risk.

Result: The status endpoint works with authentication; submission and validation logic require refinement.

## Overall results
Total tests run: 10
Passed: 6
Failed: 4
Blocked: 0

## Key findings
Health: Endpoints are stable and reliable.
• Authentication: Valid OTP works; invalid OTP returns 400 instead of 401.
• Application submission: Valid payloads rejected; validation errors obscured by duplicate logic.
• Security: The Status endpoint exposes data without authentication.

## Abandoning the flow halfway
• The UI does not provide a logout option during the loan application process.
• Users must continue until completion.
• The only alternatives are to kill the session (which generates a new session ID) or close the browser.
• If the user reaches the personal profile page and clicks back, they are redirected to the Chrome home screen.

## Retries
• 	Unable to verify retry handling since no timeout issues occurred during testing.
• 	No retry logic was observed in the current environment.

## Rate limits
• 	When sending multiple API requests, the system does not return HTTP 429 (Too Many Requests).
• 	Instead, repeated requests consistently return HTTP 401 (Unauthorized).
• 	OTP verification with correct details consistently returns HTTP 200, and each attempt generates a new session ID.

## National ID reuse
• 	The system does not validate the uniqueness of National IDs.
• 	Multiple customers can successfully apply for loans using the same ID number.

## Defects and gaps(API Testing)
• Submission rejection with 400 for valid payloads:
• Impact: Cannot confirm successful submission with valid data.
• Recommendation: Clarify business rules for duplicates vs validation.

## Validation errors not returned:
• Impact: Field-level validation feedback is missing.
• Recommendation: Return a structured errors object for invalid payloads.

## Invalid OTP returns 400 instead of 401:
• Impact: Misalignment with authentication standards.
• Recommendation: Use 401 for invalid credentials.

##Status endpoint accessible without auth:
• Impact: Sensitive data exposure risk.
• Recommendation: Enforce authentication consistently.

## BUGS
##Incorrect Time Format on Summary Page
• Date displays correctly, but time is shown in UTC format instead of local time.

##Loan Term Selection Issue
• The default loan term is set to 15 days, but on submitting, the system prompts: “Please select loan term,” even though it is already selected.

##Session Handling Problem
• Session does not expire as expected.
• Refreshing the page redirects to the start application page, then back to the personal details page inconsistently.
• Also, a person can use a previous session ID and the customer can get an approved loan??? don't know if this should be considered as a bug...

##Invalid Details Submission
• When incorrect details are entered, the user can still proceed to the next screen.
• No error message is displayed, leaving the user unaware of what went wrong.

##Duplicate ID with Different Phone Number
• If the same ID number is used with a different phone number, loan disbursement still occurs.
• This bypasses validation checks.

##Duplicate ID Loan Access
• Customers should not be allowed to access a loan using the same ID number more than once.
• Validation is missing to prevent duplicate loan applications.

##Loan Amount validation
• The system currently allows loan amounts with fractional cents (e.g., 1000.999), which is invalid.
• System should reject the input and return a validation error (e.g., 400 Bad Request with message “Invalid loan amount format”).

##Phone Number Validation
• A 13‑digit phone number starting with +256 or +254 is currently accepted, and the loan is approved.
• This should not be allowed — the maximum permitted length for numbers beginning with +256 or 254 should be 12 digits.

##Edge Cases
##Loan Amount
• The system currently allows loan amounts with fractional cents (e.g., 1000.999), which is invalid.

##Latest Date Selection
• When the latest possible date is chosen, check if the disbursement occurs or if navigation to the next screen is allowed.(This should be looked at)
• Currently, loan disbursement fails (“Could not disburse loan”).

##Wrong number plus correct OTP
• It returns a 401 UNAUTHORIZED. Which should be the expected scenario.

## Date Validation
• Customers who are 17 Years old. The loan cannot be submitted for approval.
• customers whose date of birth is 1900 can still go through the submission process, and their loan remains pending.

##Age Restriction
• Applicants aged 17 years or younger should not be able to access a loan.
• Validation must enforce the minimum age requirement.

##Phone Number Format Duplication
• Using +256 and then 256 allows the customer to receive a loan twice.
• This duplication should not be permitted.

##Future Date Usage
• Entering a future date results in loan disbursement failure (“Could not disburse loan”).
• The system should prevent the selection of future dates entirely.

##Extreme Input Lengths
• Extremely long values are accepted, and loans are still disbursed.
• Input fields should enforce maximum length restrictions.

##Duplicate ID Numbers
• Customers can access loans using duplicate ID numbers.
• Validation should block loan approval when the same ID is reused.

##Invalid Endpoint Handling
• Calling an invalid endpoint correctly returns 404.
• This behavior is working as expected.

##Incorrect Request Body Status
• Submitting an incorrect request body currently returns 401.
• Expected status should be 400 (Bad Request).

##Incorrect Phone Number in OTP Request
• Entering an invalid phone number in OTP request returns 401.
• Expected status should be 400 (Bad Request).

##Phone Number Validation
• A 13‑digit phone number starting with +256 or +254 is currently accepted, and the loan is approved.
• This should not be allowed — the maximum permitted length for numbers beginning with +256 or 254 should be 12 digits.

## Recommendations
• Align error schemas: Use errors for validation, 401 for auth failures.
• Enforce auth: Protect status endpoints.
• Deduplicate smartly: Return validation errors before duplicate checks.

## Phone Number Validation
• Ensure the phone number field enforces country-specific formats (e.g., must start with +254 or +256).
• Display a validation error message if the format is incorrect.
• Restrict input to a maximum of 12 digits.
• Automatically prepend + when a user enters a number without it.

## Date of Birth (DOB) Validation
• If incorrect DOB details are entered, display a clear error message before submission.
• Enforce an age restriction: applicants must be 18 years or older.
• The date picker should default to valid ranges (e.g., DOB must be at least 18 years prior to today).
• Prevent selection of future dates.

## Full Name Validation
Restrict the field from accepting numeric characters.
If numbers are entered, display a validation error message.

## National ID Validation
• Enforce maximum length rules:
  Uganda (UG): 14 digits
  Kenya (KE): minimum 10 digits
• Display a clear error message if the input exceeds or falls short of the required length.
• If the ID number already exists in the system, return a validation error: “ID number already in use.”

## Loan Amount Validation
• Set minimum and maximum loan amounts based on the applicant’s age and predefined conditions.
• Display appropriate error messages when the entered amount is outside the allowed range.

## Loan Purpose Field
• Requires a minimum word count before submission.
• If the requirement is not met, display a message indicating how many words are still needed.

## Form Submission Rules
• If any incorrect details are entered, prevent navigation to the next screen.
• Display inline error messages highlighting the specific fields with issues.

## What I decide not to automate.
## Expired OTP
• Difficult to test because the OTP is hardcoded.
• This scenario is better suited for exploratory and manual testing.

## Multiple OTP Resends
• Low frequency of occurrence adds complexity to automation.
• Recommend handling through manual testing to validate behavior.

## Invalid OTP Entry
• User enters an incorrect OTP (negative test case).
• Useful to test manually to observe how the system responds and communicates errors.

• Some scenarios related to borrower age and loan eligibility were not automated in this test.
• These cases have been intentionally left for manual testing to ensure proper validation of age restrictions and edge cases.

## Conclusion
The automated QA suite for the Numida Loan Application API provided valuable insights into system behavior, validation rules, and security enforcement.

## Strength
• Health check endpoints are stable and confirm API availability.
• Authentication works correctly for valid OTPs.
• Loan application status endpoint functions as expected when authenticated.

## Weakness and Gaps
• Invalid OTPs return 400 Bad Request instead of 401 Unauthorized, misaligning with standard authentication practices.
• HTTP Duplicate check CODE are not captured well.
• Phone number validation allows 13 digits with +256 or +254 prefix, though the maximum should be 12.
• Age-related loan eligibility scenarios were not automated and are left for manual testing.


```json
{
  "message": "See you soon, chao!May the force be with you."
}
```

