import json
import pytest
from app.models.summary_history import SummaryHistory, StatusEnum
from datetime import datetime, timedelta

def test_create_summary_history(client, db):
    """Test creating a summary history record."""
    # Test data
    data = {
        "email": "test@example.com",
        "status": StatusEnum.START,
        "channels": "general",
        "notion_page_url": "https://notion.so/page-id"
    }
    
    # Send POST request
    response = client.post(
        '/api/summary-histories',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    # Check response
    assert response.status_code == 201
    json_data = json.loads(response.data)
    assert json_data['email'] == data['email']
    assert json_data['status'] == data['status']
    assert json_data['channels'] == data['channels']
    
    # Verify database entry
    history = SummaryHistory.query.filter_by(email=data['email']).first()
    assert history is not None
    assert history.status == data['status']
    assert history.notion_page_url == data['notion_page_url']

def test_update_summary_history(client, db):
    """Test updating a summary history record."""
    # Create test data
    now = datetime.utcnow()
    history = SummaryHistory(
        email="update-test@example.com",
        status=StatusEnum.START,
        start_time=now,
    )
    db.session.add(history)
    db.session.commit()
    
    # Get the ID
    history_id = history.id
    
    # Update data
    update_data = {
        "id": history_id,
        "email": "update-test@example.com",
        "status": StatusEnum.SUCCESS,
        "end_time": (now + timedelta(minutes=5)).isoformat(),
        "notion_page_url": "https://notion.so/updated-page"
    }
    
    # Send POST request (uses same endpoint with ID to update)
    response = client.post(
        '/api/summary-histories',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    
    # Check response
    assert response.status_code == 200
    json_data = json.loads(response.data)
    assert json_data['email'] == update_data['email']
    assert json_data['status'] == update_data['status']
    assert json_data['notion_page_url'] == update_data['notion_page_url']
    
    # Verify database update
    updated_history = SummaryHistory.query.get(history_id)
    assert updated_history.status == update_data['status']
    assert updated_history.notion_page_url == update_data['notion_page_url']
    assert updated_history.end_time is not None

def test_get_summary_histories(client, db):
    """Test getting summary histories."""
    # Create test data
    email = "list-test@example.com"
    now = datetime.utcnow()
    
    histories = [
        SummaryHistory(
            email=email,
            status=StatusEnum.SUCCESS,
            start_time=now - timedelta(days=i),
            end_time=now - timedelta(days=i, minutes=-30),
            notion_page_url=f"https://notion.so/page-{i}"
        )
        for i in range(5)
    ]
    
    db.session.add_all(histories)
    db.session.commit()
    
    # Send GET request
    response = client.get(f'/api/summary-histories?email={email}&limit=3&page=1')
    
    # Check response
    assert response.status_code == 200
    json_data = json.loads(response.data)
    assert json_data['total'] == 5
    assert len(json_data['histories']) == 3
    assert json_data['page'] == 1
    assert json_data['limit'] == 3
    
    # Page 2 should have the remaining 2 records
    response = client.get(f'/api/summary-histories?email={email}&limit=3&page=2')
    json_data = json.loads(response.data)
    assert len(json_data['histories']) == 2

def test_get_specific_summary_history(client, db):
    """Test getting a specific summary history by ID."""
    # Create test data
    history = SummaryHistory(
        email="specific-test@example.com",
        status=StatusEnum.SUCCESS,
        start_time=datetime.utcnow(),
        end_time=datetime.utcnow(),
        channels="channel1",
        notion_page_url="https://notion.so/specific-page"
    )
    
    db.session.add(history)
    db.session.commit()
    
    # Get the ID
    history_id = history.id
    
    # Send GET request
    response = client.get(f'/api/summary-histories/{history_id}')
    
    # Check response
    assert response.status_code == 200
    json_data = json.loads(response.data)
    assert json_data['id'] == history_id
    assert json_data['email'] == history.email
    assert json_data['status'] == history.status
    assert json_data['channels'] == history.channels
    assert json_data['notion_page_url'] == history.notion_page_url

def test_get_nonexistent_summary_history(client):
    """Test getting a nonexistent summary history."""
    # Invalid ID
    history_id = 9999
    
    # Send GET request
    response = client.get(f'/api/summary-histories/{history_id}')
    
    # Check response - should be not found
    assert response.status_code == 404 