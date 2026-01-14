# Test Plan Document – Numida Loan Application

## 1. Introduction
This test plan defines the QA strategy for validating the Numida loan application system, focusing on API Testing, OTP authentication, personal details entry, loan submission, and decision rules(Approved/Pending).

## 2. Objectives
- Verify functional correctness of loan application workflows.
- Validate business rules (e.g., Pending for high-value loans).
- Identify gaps in validation (e.g., duplicate National IDs).
- Document system behaviors under edge cases.
- What happens if the user abandons the flow halfway?
- How are retries handled?
- Are there rate limits?
- What happens if the same National ID is reused?
- Duplicate submission handling
- Session management
- Error handling consistency
- Status persistence:


## 3. Scope
### In Scope
- OTP request and validation.
- Personal details entry.
- Loan details submission.
- Loan decision messages (Approved, Pending).
- Session handling and navigation.
- Loan amount validation(Decimal precision).
- Duplicate submission handling.
- National ID reuse checks.

### Out of Scope
- Retry handling (not observed in test environment)
- Rate limiting (no HTTP 429 responses observed) should be considered as future coverage area.

## 4. Test Items
- UI workflows (Selenium automation, test_loanApp.py)
- API endpoints (test_healthcheck.py, test_authentication.py, 			         test_application.py)
- Test data (`test_loanApp.json`, `test_apiData.json`)

## 5. Test Approach
- Manual exploratory testing.
- Automated tests using Pytest + Selenium
- Data-driven tests with JSON input.
- System testing End to End
- Exploratory testing.

## 6. Test Environment
- Windows 11, Chrome browser, firefox browser
- Python 3.13, Pytest 9.0
- Test environment provided by Numida.

## 7. Entry/Exit Criteria
- Entry: Environment setup complete, test data prepared.
- Exit: All in-scope test cases executed, defects logged.

## 8. Test Cases
 - Loan amount 2 decimals or more should fail (Currently passes)
 - Duplicate submission => Should return 409 conflicts (Currently returning 400)
 - Session Expiry => Session should expire after a specified period of time e.g 1 hour
 - Request OTP invalid phone => should return 401 (Currently 400).
 - Wrong number + correct OTP => Correctly returns 401(Expected)
 - National ID reuse => Should fail (currently allowed).
 - Rate limiting => Should return 429 (Currently 401).
 - Retry Handling => Behavior unclear marked as Gap.
 - Abandonment => no graceful exit, only browser close.


## 9. Risks & Assumptions
- Retry logic not verified due to no timeout issues.
- Rate limits unclear; repeated requests returned 401 instead of 429.
- National ID uniqueness not enforced.

## 10. Deliverables
- Automated test scripts
- README.md with findings
- Defect logs and observations
