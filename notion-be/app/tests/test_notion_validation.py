import json
import pytest
from unittest.mock import patch, MagicMock
from app.models.app_setting import AppSetting

def test_validate_notion_connection_success(client):
    """Test successful Notion connection validation."""
    with patch('app.api.notion_validation.NotionManager') as mock_notion_manager:
        # Configure the mock
        instance = mock_notion_manager.return_value
        instance.validate_connection.return_value = True
        instance._format_page_id.return_value = "8a9b2c3d-4e5f-6g7h-8i9j-0k1l2m3n4o5p"
        
        # Test data
        data = {
            "notion_secret": "test-notion-secret",
            "notion_page_id": "8a9b2c3d4e5f6g7h8i9j0k1l2m3n4o5p"
        }
        
        # Send POST request
        response = client.post(
            '/api/notion/validate-connection',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Check response
        assert response.status_code == 200
        json_data = json.loads(response.data)
        assert json_data['success'] is True
        assert "Successfully connected" in json_data['message']
        
        # Verify the mock was called with correct arguments
        mock_notion_manager.assert_called_once_with(api_key=data['notion_secret'])
        instance.validate_connection.assert_called_once()
        instance._format_page_id.assert_called_once_with(data['notion_page_id'])

def test_validate_notion_connection_invalid_key(client):
    """Test Notion connection validation with invalid API key."""
    with patch('app.api.notion_validation.NotionManager') as mock_notion_manager:
        # Configure the mock to raise an exception
        instance = mock_notion_manager.return_value
        instance.validate_connection.side_effect = ValueError("Unauthorized: Your API key is invalid")
        
        # Test data
        data = {
            "notion_secret": "invalid-notion-secret",
            "notion_page_id": "8a9b2c3d4e5f6g7h8i9j0k1l2m3n4o5p"
        }
        
        # Send POST request
        response = client.post(
            '/api/notion/validate-connection',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Check response
        assert response.status_code == 400
        json_data = json.loads(response.data)
        assert json_data['success'] is False
        assert "invalid" in json_data['message'].lower()

def test_validate_notion_connection_missing_data(client):
    """Test Notion connection validation with missing data."""
    # Test with missing notion_secret
    data1 = {
        "notion_page_id": "8a9b2c3d4e5f6g7h8i9j0k1l2m3n4o5p"
    }
    
    response1 = client.post(
        '/api/notion/validate-connection',
        data=json.dumps(data1),
        content_type='application/json'
    )
    
    assert response1.status_code == 400
    json_data1 = json.loads(response1.data)
    assert json_data1['success'] is False
    assert "notion secret key is required" in json_data1['message'].lower()
    
    # Test with missing notion_page_id
    data2 = {
        "notion_secret": "test-notion-secret"
    }
    
    response2 = client.post(
        '/api/notion/validate-connection',
        data=json.dumps(data2),
        content_type='application/json'
    )
    
    assert response2.status_code == 400
    json_data2 = json.loads(response2.data)
    assert json_data2['success'] is False
    assert "notion page id is required" in json_data2['message'].lower()

def test_update_notion_settings(client, db):
    """Test updating Notion settings."""
    # Create test data
    email = "notion-test@example.com"
    setting = AppSetting(
        email=email,
        schedule_period="weekly",
        notion_secret="old-secret",
        notion_page_id="old-page-id"
    )
    db.session.add(setting)
    db.session.commit()
    
    # Update data
    update_data = {
        "email": email,
        "notion_secret": "new-secret",
        "notion_page_id": "new-page-id"
    }
    
    # Send PUT request
    response = client.put(
        '/api/app-settings/notion',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    
    # Check response
    assert response.status_code == 200
    json_data = json.loads(response.data)
    assert json_data['email'] == email
    assert json_data['notion_secret'] == "new-secret"
    assert json_data['notion_page_id'] == "new-page-id"
    
    # Verify database update
    updated_setting = AppSetting.query.get(email)
    assert updated_setting.notion_secret == "new-secret"
    assert updated_setting.notion_page_id == "new-page-id"

def test_update_notion_settings_missing_email(client):
    """Test updating Notion settings with missing email."""
    update_data = {
        "notion_secret": "new-secret",
        "notion_page_id": "new-page-id"
    }
    
    response = client.put(
        '/api/app-settings/notion',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    
    assert response.status_code == 400
    json_data = json.loads(response.data)
    assert "email is required" in json_data['error'].lower()

def test_update_notion_settings_nonexistent_email(client, db):
    """Test updating Notion settings for nonexistent email."""
    update_data = {
        "email": "nonexistent@example.com",
        "notion_secret": "new-secret",
        "notion_page_id": "new-page-id"
    }
    
    response = client.put(
        '/api/app-settings/notion',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    
    assert response.status_code == 404
    json_data = json.loads(response.data)
    assert "no app settings found" in json_data['error'].lower()

def test_update_slack_settings(client, db):
    """Test updating Slack settings."""
    # Create test data
    email = "slack-test@example.com"
    setting = AppSetting(
        email=email,
        schedule_period="weekly",
        slack_token="old-token"
    )
    db.session.add(setting)
    db.session.commit()
    
    # Update data
    update_data = {
        "email": email,
        "slack_token": "new-token"
    }
    
    # Send PUT request
    response = client.put(
        '/api/app-settings/slack',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    
    # Check response
    assert response.status_code == 200
    json_data = json.loads(response.data)
    assert json_data['email'] == email
    assert json_data['slack_token'] == "new-token"
    
    # Verify database update
    updated_setting = AppSetting.query.get(email)
    assert updated_setting.slack_token == "new-token"

def test_update_slack_settings_missing_email(client):
    """Test updating Slack settings with missing email."""
    update_data = {
        "slack_token": "new-token"
    }
    
    response = client.put(
        '/api/app-settings/slack',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    
    assert response.status_code == 400
    json_data = json.loads(response.data)
    assert "email is required" in json_data['error'].lower()

def test_update_slack_settings_missing_token(client):
    """Test updating Slack settings with missing token."""
    update_data = {
        "email": "test@example.com"
    }
    
    response = client.put(
        '/api/app-settings/slack',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    
    assert response.status_code == 400
    json_data = json.loads(response.data)
    assert "slack_token is required" in json_data['error'].lower()

def test_update_slack_settings_nonexistent_email(client, db):
    """Test updating Slack settings for nonexistent email."""
    update_data = {
        "email": "nonexistent@example.com",
        "slack_token": "new-token"
    }
    
    response = client.put(
        '/api/app-settings/slack',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    
    assert response.status_code == 404
    json_data = json.loads(response.data)
    assert "no app settings found" in json_data['error'].lower() 