import json
import pytest
from unittest.mock import patch
from app.models.app_setting import AppSetting
from app.models.summary_history import SummaryHistory

@patch('app.api.summary.create_notion_summary')
def test_trigger_summary(mock_create_notion_summary, client, db):
    """Test triggering a summary process."""
    # Mock the Notion API call
    mock_create_notion_summary.return_value = {"success": True, "page_url": "https://notion.so/test-page"}
    
    # Create app settings first (required for the trigger)
    email = "trigger-test@example.com"
    app_setting = AppSetting(
        email=email,
        schedule_period="daily",
        default_channels="channel1",
        slack_token="test-token",
        notion_secret="test-secret",
        notion_page_id="test-page-id"
    )
    db.session.add(app_setting)
    db.session.commit()
    
    # Test data
    data = {
        "email": email,
        "channels": "custom-channel"
    }
    
    # Send POST request
    response = client.post(
        '/api/summary/trigger',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    # Check response
    assert response.status_code == 202
    json_data = json.loads(response.data)
    assert "trigger_id" in json_data
    assert "summary" in json_data
    assert json_data["summary"]["email"] == email
    assert json_data["summary"]["status"] == "start"
    assert json_data["summary"]["channels"] == "custom-channel"
    
    # Verify database entry
    history = SummaryHistory.query.get(json_data["trigger_id"])
    assert history is not None
    assert history.status == "start"
    assert history.email == email
    assert history.channels == "custom-channel"

def test_trigger_summary_no_app_settings(client):
    """Test triggering a summary without app settings."""
    email = "no-settings@example.com"
    
    # Test data
    data = {
        "email": email
    }
    
    # Send POST request
    response = client.post(
        '/api/summary/trigger',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    # Check response - should fail without app settings
    assert response.status_code == 404

def test_trigger_summary_missing_email(client):
    """Test triggering a summary without providing an email."""
    # Test data with missing email
    data = {
        "channels": "custom-channel"
    }
    
    # Send POST request
    response = client.post(
        '/api/summary/trigger',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    # Check response - should fail without email
    assert response.status_code == 400 