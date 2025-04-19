import json
import pytest
from datetime import datetime, timedelta
from app.models.summary_history import SummaryHistory, StatusEnum

def test_get_latest_summary_without_email(client):
    """Test getting the latest summary history without providing an email."""
    response = client.get('/api/summary/latest')
    
    assert response.status_code == 400
    json_data = json.loads(response.data)
    assert "error" in json_data
    assert "Email parameter is required" in json_data["error"]

def test_get_latest_summary_nonexistent_email(client):
    """Test getting the latest summary history for an email with no summaries."""
    response = client.get('/api/summary/latest?email=nonexistent@example.com')
    
    assert response.status_code == 404
    json_data = json.loads(response.data)
    assert "error" in json_data
    assert "No summary history found for this email" in json_data["error"]

def test_get_latest_summary_history(client, db):
    """Test getting the latest summary history for an email with multiple summaries."""
    # Create test data
    email = "latest-test@example.com"
    now = datetime.utcnow()
    
    # Create several history entries with different timestamps
    histories = [
        SummaryHistory(
            email=email,
            status=StatusEnum.SUCCESS,
            start_time=now - timedelta(days=3),
            end_time=now - timedelta(days=3, minutes=-30),
            notion_page_url="https://notion.so/page-oldest"
        ),
        SummaryHistory(
            email=email,
            status=StatusEnum.FAILED,
            start_time=now - timedelta(days=2),
            end_time=now - timedelta(days=2, minutes=-30),
            notion_page_url="https://notion.so/page-middle"
        ),
        SummaryHistory(
            email=email,
            status=StatusEnum.START,
            start_time=now - timedelta(days=1),
            channels=json.dumps(["channel1", "channel2"]),
            notion_page_url="https://notion.so/page-latest"
        )
    ]
    
    db.session.add_all(histories)
    db.session.commit()
    
    # Send GET request to get the latest summary
    response = client.get(f'/api/summary/latest?email={email}')
    
    # Check response
    assert response.status_code == 200
    json_data = json.loads(response.data)
    
    # Should return the most recent history (from 1 day ago)
    assert json_data['email'] == email
    assert json_data['status'] == StatusEnum.START
    assert json_data['notion_page_url'] == "https://notion.so/page-latest"
    
    # Create an even newer entry
    newest_history = SummaryHistory(
        email=email,
        status=StatusEnum.IN_PROGRESS,
        start_time=now,
        channels=json.dumps(["channel3"]),
        notion_page_url="https://notion.so/page-newest"
    )
    db.session.add(newest_history)
    db.session.commit()
    
    # Send GET request again
    response = client.get(f'/api/summary/latest?email={email}')
    
    # Check response
    assert response.status_code == 200
    json_data = json.loads(response.data)
    
    # Should return the newest history entry now
    assert json_data['email'] == email
    assert json_data['status'] == StatusEnum.IN_PROGRESS
    assert json_data['notion_page_url'] == "https://notion.so/page-newest" 