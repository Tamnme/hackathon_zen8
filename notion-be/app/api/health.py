from flask import jsonify
from app.api import api_bp
from app.models import db

@api_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for monitoring the service.
    Returns status of the API and database connection.
    """
    health_status = {
        'status': 'healthy',
        'api': True
    }
    
    # Check database connection
    try:
        db.session.execute('SELECT 1')
        health_status['database'] = True
    except Exception as e:
        health_status['database'] = False
        health_status['status'] = 'degraded'
        health_status['db_error'] = str(e)
    
    return jsonify(health_status) 