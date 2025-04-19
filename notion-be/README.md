# Notion & Slack Integration API

This API service provides functionality to manage integration between Notion and Slack, allowing users to store third-party secrets, trigger analytics processes, and schedule automated triggers.

## Features

- Store and manage application settings (Notion and Slack tokens)
- Configure trigger settings for automated processes
- Trigger summary generation manually
- View history of summary processes
- RESTful API endpoints for integration with other services

## Technology Stack

- Python 3.x
- Flask web framework
- SQLite database
- SQLAlchemy ORM
- Flask-Migrate for database migrations

## Project Structure

```
python/
├── app/
│   ├── api/                   # API endpoints
│   ├── config/                # Configuration settings
│   ├── models/                # Database models
│   └── tests/                 # Test cases
├── Contracts/                 # Postman API contracts
├── run.py                     # Application entry point
├── requirements.txt           # Project dependencies
└── README.md                  # Documentation
```

## Setup Instructions

### Prerequisites

- Python 3.x
- pip3

### Installation

1. Clone the repository
2. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip3 install -r requirements.txt
```

4. Run the application:

```bash
python run.py
```

The API will be available at `http://localhost:8080`.

### Docker Setup

#### Prerequisites
- Docker
- Docker Compose

#### Running with Docker Compose

1. Copy the example environment file and modify as needed:
   ```bash
   cp .env.example .env
   ```

2. Update the environment variables in `.env` file with your Notion API credentials:
   ```
   NOTION_API_KEY=your_notion_api_key_here
   NOTION_DATABASE_ID=your_notion_database_id_here
   ```

3. Build and start the containers:
   ```bash
   docker-compose up -d
   ```

   This will start:
   - The Flask application on port 8080
   - PostgreSQL database on port 5432

4. Check the container status:
   ```bash
   docker-compose ps
   ```

5. View logs:
   ```bash
   docker-compose logs -f
   ```

6. Stop the containers:
   ```bash
   docker-compose down
   ```

7. To completely reset (including database volume):
   ```bash
   docker-compose down -v
   ```

The API will be available at `http://localhost:8080`.

## API Endpoints

### App Settings

- `GET /api/app-settings?email=<email>` - Get app settings for a user
- `POST /api/app-settings` - Create app settings
- `PUT /api/app-settings/<email>` - Update app settings

### Trigger Settings

- `GET /api/trigger-settings?email=<email>` - Get trigger settings for a user
- `POST /api/trigger-settings` - Create trigger settings
- `PUT /api/trigger-settings/<id>` - Update trigger settings

### Summary Histories

- `GET /api/summary-histories?email=<email>&limit=<limit>&page=<page>` - Get paginated list of summaries
- `GET /api/summary-histories/<id>` - Get a specific summary history
- `POST /api/summary-histories` - Create or update a summary history

### Trigger Summary

- `POST /api/summary/trigger` - Trigger a summary process

## Running Tests

```bash
pytest
```

## API Contracts

API contract documentation is available in the `Contracts` folder as Postman collection JSON files:

- `app_settings.json` - Contracts for app settings endpoints
- `trigger_settings.json` - Contracts for trigger settings endpoints
- `summary_histories.json` - Contracts for summary histories endpoints
- `summary_trigger.json` - Contract for summary trigger endpoint

## Development Status

- ✅ Core API functionality implemented
- ✅ Model relationships established
- ✅ All tests passing
- ✅ Postman API contracts created
- ⬜ Authentication system (future enhancement)
- ⬜ User management (future enhancement)
- ⬜ Background task processing (future enhancement)

# Notion Integration with Python

This project demonstrates how to integrate with the Notion API using Python.

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Notion API Setup

1. Go to [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Click "New integration"
3. Name your integration and select the workspace
4. After creating the integration, copy the "Internal Integration Token"
5. Open the `.env` file and set `NOTION_API_KEY` to your token:
   ```
   NOTION_API_KEY=secret_your_integration_token_here
   ```

6. Create a database in Notion or use an existing one
7. Share the database with your integration:
   - Open the database in Notion
   - Click "..." in the top-right corner
   - Select "Add connections"
   - Choose your integration
8. Get the database ID from the URL:
   - The URL format is: `https://www.notion.so/{workspace_name}/{database_id}?v={view_id}`
   - Copy the `database_id` part
9. Set the `NOTION_DATABASE_ID` in the `.env` file:
   ```
   NOTION_DATABASE_ID=your_database_id_here
   ```

## Running the Application

```bash
flask run
```

## Using the Notion Client

The project includes a `NotionManager` class in `app/services/notion_client_manager.py` for interacting with the Notion API:

```python
from app.services.notion_client_manager import NotionManager

# Initialize the client
notion = NotionManager()

# Validate connection
notion.validate_connection()

# Create database item
properties = {
    "Name": {
        "title": [{"text": {"content": "My Page Title"}}]
    }
}
content = [{
    "object": "block",
    "type": "paragraph",
    "paragraph": {
        "rich_text": [{"text": {"content": "Hello, Notion!"}}]
    }
}]

new_page = notion.create_database_item(database_id, properties, content)
```

## Troubleshooting

- If you get an authentication error, make sure your API key is correct and starts with `secret_`
- If you get a "page not found" error, make sure you've shared the database with your integration
- If you need more detailed error information, check the Notion API documentation at [https://developers.notion.com](https://developers.notion.com) 