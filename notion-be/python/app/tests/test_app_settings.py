import json
import pytest
from app.models.app_setting import AppSetting

def test_create_app_settings(client, db):
    """Test creating app settings."""
    # Test data
    data = {
        "email": "test@example.com",
        "schedule_period": "daily",
        "default_channels": "general",
        "get_notion_page": "method1",
        "slack_token": "xoxb-test-token",
        "notion_secret": "test-notion-secret",
        "notion_page_id": "test-page-id"
    }
    
    # Send POST request
    response = client.post(
        '/api/app-settings',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    # Check response
    assert response.status_code == 201
    json_data = json.loads(response.data)
    assert json_data['email'] == data['email']
    assert json_data['slack_token'] == data['slack_token']
    
    # Verify database entry
    setting = AppSetting.query.get(data['email'])
    assert setting is not None
    assert setting.notion_page_id == data['notion_page_id']

def test_get_app_settings(client, db):
    """Test getting app settings."""
    # Create test data
    email = "get-test@example.com"
    setting = AppSetting(
        email=email,
        schedule_period="weekly",
        slack_token="test-token"
    )
    db.session.add(setting)
    db.session.commit()
    
    # Send GET request
    response = client.get(f'/api/app-settings?email={email}')
    
    # Check response
    assert response.status_code == 200
    json_data = json.loads(response.data)
    assert json_data['email'] == email
    assert json_data['schedule_period'] == "weekly"
    
def test_get_nonexistent_app_settings(client):
    """Test getting app settings for nonexistent email."""
    email = "nonexistent@example.com"
    
    # Send GET request
    response = client.get(f'/api/app-settings?email={email}')
    
    # Check response
    assert response.status_code == 404

def test_update_app_settings(client, db):
    """Test updating app settings."""
    # Create test data
    email = "update-test@example.com"
    setting = AppSetting(
        email=email,
        schedule_period="weekly",
        slack_token="old-token"
    )
    db.session.add(setting)
    db.session.commit()
    
    # Update data
    update_data = {
        "schedule_period": "daily",
        "slack_token": "new-token"
    }
    
    # Send PUT request
    response = client.put(
        f'/api/app-settings/{email}',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    
    # Check response
    assert response.status_code == 200
    json_data = json.loads(response.data)
    assert json_data['email'] == email
    assert json_data['schedule_period'] == "daily"
    assert json_data['slack_token'] == "new-token"
    
    # Verify database update
    updated_setting = AppSetting.query.get(email)
    assert updated_setting.schedule_period == "daily"
    assert updated_setting.slack_token == "new-token"

def test_create_duplicate_app_settings(client, db):
    """Test creating duplicate app settings."""
    # Create initial settings
    email = "duplicate@example.com"
    setting = AppSetting(
        email=email,
        schedule_period="weekly"
    )
    db.session.add(setting)
    db.session.commit()
    
    # Try to create duplicate
    data = {
        "email": email,
        "schedule_period": "daily"
    }
    
    # Send POST request
    response = client.post(
        '/api/app-settings',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    # Check response - should be conflict
    assert response.status_code == 409 