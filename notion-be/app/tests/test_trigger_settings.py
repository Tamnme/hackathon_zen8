import json
import pytest
from app.models.trigger_setting import TriggerSetting
from datetime import date

def test_create_trigger_settings(client, db):
    """Test creating trigger settings."""
    # Test data
    data = {
        "email": "test@example.com",
        "channels": "general,random",
        "start_date": "2023-01-01",
        "end_date": "2023-12-31"
    }
    
    # Send POST request
    response = client.post(
        '/api/trigger-settings',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    # Check response
    assert response.status_code == 201
    json_data = json.loads(response.data)
    assert json_data['email'] == data['email']
    assert json_data['channels'] == data['channels']
    assert json_data['start_date'] == data['start_date']
    assert json_data['end_date'] == data['end_date']
    
    # Verify database entry
    settings = TriggerSetting.query.filter_by(email=data['email']).first()
    assert settings is not None
    assert settings.channels == data['channels']
    assert settings.start_date == date(2023, 1, 1)
    assert settings.end_date == date(2023, 12, 31)

def test_get_trigger_settings(client, db):
    """Test getting trigger settings."""
    # Create test data
    email = "get-test@example.com"
    setting = TriggerSetting(
        email=email,
        channels="channel1",
        start_date=date(2023, 1, 1),
        end_date=date(2023, 12, 31)
    )
    db.session.add(setting)
    db.session.commit()
    
    # Send GET request
    response = client.get(f'/api/trigger-settings?email={email}')
    
    # Check response
    assert response.status_code == 200
    json_data = json.loads(response.data)
    assert len(json_data) == 1
    assert json_data[0]['email'] == email
    assert json_data[0]['channels'] == "channel1"
    assert json_data[0]['start_date'] == "2023-01-01"
    
def test_get_multiple_trigger_settings(client, db):
    """Test getting multiple trigger settings for same email."""
    # Create test data
    email = "multiple@example.com"
    
    setting1 = TriggerSetting(
        email=email,
        channels="channel1",
        start_date=date(2023, 1, 1),
        end_date=date(2023, 6, 30)
    )
    
    setting2 = TriggerSetting(
        email=email,
        channels="channel2",
        start_date=date(2023, 7, 1),
        end_date=date(2023, 12, 31)
    )
    
    db.session.add_all([setting1, setting2])
    db.session.commit()
    
    # Send GET request
    response = client.get(f'/api/trigger-settings?email={email}')
    
    # Check response
    assert response.status_code == 200
    json_data = json.loads(response.data)
    assert len(json_data) == 2
    
def test_update_trigger_settings(client, db):
    """Test updating trigger settings."""
    # Create test data
    email = "update-test@example.com"
    setting = TriggerSetting(
        email=email,
        channels="old-channel",
        start_date=date(2023, 1, 1),
        end_date=date(2023, 12, 31)
    )
    db.session.add(setting)
    db.session.commit()
    
    # Get the ID
    setting_id = setting.id
    
    # Update data
    update_data = {
        "channels": "new-channel",
        "start_date": "2023-02-01"
    }
    
    # Send PUT request
    response = client.put(
        f'/api/trigger-settings/{setting_id}',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    
    # Check response
    assert response.status_code == 200
    json_data = json.loads(response.data)
    assert json_data['email'] == email
    assert json_data['channels'] == "new-channel"
    assert json_data['start_date'] == "2023-02-01"
    
    # Verify database update
    updated_setting = TriggerSetting.query.get(setting_id)
    assert updated_setting.channels == "new-channel"
    assert updated_setting.start_date == date(2023, 2, 1)
    assert updated_setting.end_date == date(2023, 12, 31)  # Unchanged

def test_update_nonexistent_trigger_settings(client):
    """Test updating nonexistent trigger settings."""
    # Invalid ID
    setting_id = 9999
    
    # Update data
    update_data = {
        "channels": "new-channel"
    }
    
    # Send PUT request
    response = client.put(
        f'/api/trigger-settings/{setting_id}',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    
    # Check response - should be not found
    assert response.status_code == 404 