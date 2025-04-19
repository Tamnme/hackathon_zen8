from app import create_app
from app.models import db

app = create_app()

# Create the database tables if they don't exist yet
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080) 