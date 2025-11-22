from fastapi.testclient import TestClient
from app.main import app
from datetime import datetime
import re

client = TestClient(app)

def test_create_code():
    response = client.post("/api/v1/codes", json={"owner": "test_user", "ttl_seconds": 3600})
    assert response.status_code == 200
    
    data = response.json()
    assert "central_id" in data
    assert "expires_at" in data
    
    # Verify central_id is 12 uppercase hex characters
    central_id = data["central_id"]
    assert len(central_id) == 12
    assert re.match(r"^[0-9A-F]{12}$", central_id)
    
    # Verify expires_at is a valid future ISO timestamp
    expires_at_str = data["expires_at"]
    expires_at = datetime.fromisoformat(expires_at_str)
    assert expires_at > datetime.now(expires_at.tzinfo)
