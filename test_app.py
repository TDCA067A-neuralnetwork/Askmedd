from app import app


def test_home_page():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"Clinical Question Answering System" in response.data


def test_health():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_non_medical_question_is_rejected():
    client = app.test_client()
    response = client.post("/api/ask", json={"question": "Tell me a joke"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["allowed"] is False
    assert data["classification"] == "non-medical"
