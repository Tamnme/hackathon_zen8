from flask import jsonify, request
from app.api import api_bp
from app.models import db
from app.models.summary_history import SummaryHistory
from datetime import datetime

@api_bp.route('/summary-histories', methods=['GET'])
def get_summary_histories():
    """Get paginated summary histories for an email."""
    email = request.args.get('email')
    limit = request.args.get('limit', 10, type=int)
    page = request.args.get('page', 1, type=int)
    
    if not email:
        return jsonify({"error": "Email parameter is required"}), 400
    
    query = SummaryHistory.query.filter_by(email=email)
    total = query.count()
    
    histories = query.order_by(SummaryHistory.start_time.desc()) \
                    .limit(limit).offset((page - 1) * limit).all()
    
    return jsonify({
        "histories": [history.to_dict() for history in histories],
        "page": page,
        "limit": limit,
        "total": total
    }), 200

@api_bp.route('/summary-histories/<int:history_id>', methods=['GET'])
def get_summary_history(history_id):
    """Get a specific summary history by ID."""
    history = SummaryHistory.query.get(history_id)
    
    if not history:
        return jsonify({"error": "Summary history not found"}), 404
        
    return jsonify(history.to_dict()), 200

@api_bp.route('/summary-histories', methods=['POST'])
def create_summary_history():
    """Create or update a summary history."""
    data = request.json
    
    if not data or 'email' not in data or 'status' not in data:
        return jsonify({"error": "Email and status are required fields"}), 400
        
    # Check if there's an existing record with start status
    history_id = data.get('id')
    existing = None
    
    if history_id:
        existing = SummaryHistory.query.get(history_id)
    
    if existing:
        # Update existing record
        existing.status = data['status']
        existing.end_time = datetime.fromisoformat(data['end_time']) if 'end_time' in data else None
        existing.channels = data.get('channels', existing.channels)
        existing.notion_page_url = data.get('notion_page_url', existing.notion_page_url)
        db.session.commit()
        return jsonify(existing.to_dict()), 200
    else:
        # Create new record
        new_history = SummaryHistory(
            email=data['email'],
            status=data['status'],
            start_time=datetime.fromisoformat(data['start_time']) if 'start_time' in data else datetime.utcnow(),
            end_time=datetime.fromisoformat(data['end_time']) if 'end_time' in data else None,
            channels=data.get('channels'),
            notion_page_url=data.get('notion_page_url')
        )
        db.session.add(new_history)
        db.session.commit()
        return jsonify(new_history.to_dict()), 201 