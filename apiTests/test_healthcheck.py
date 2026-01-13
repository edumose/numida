def test_health_check(base_url, api_session):
    health = api_session.get(f"{base_url}/api/health")
    assert health.status_code == 200
    body = health.json()
    assert body.get("status") == "healthy"

def test_welcome_message(base_url, api_session):
    message = api_session.get(f"{base_url}/")
    assert message.status_code == 200
    body = message.json()
    assert body.get("message") == "Welcome to the Loan Application API"
    assert body.get("version") == "1.0.0"