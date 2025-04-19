from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import logging
from main import process_channel_summary
from config.config import load_config
from features.slack_client import initialize_slack_client, get_available_channels
from features.notion_client import initialize_notion_client

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('/app/logs/api.log')
    ]
)

app = FastAPI(title="Slack-Notion Summarizer API")

# Load configuration once at startup
try:
    config = load_config()
    slack_client = initialize_slack_client(config['slack']['bot_token'])
    notion_client = initialize_notion_client(config['notion']['api_key'])
    logging.info("Successfully initialized API clients")
except Exception as e:
    logging.error(f"Failed to initialize API: {str(e)}")
    raise

class SummaryRequest(BaseModel):
    channel_name: str
    start_timestamp: datetime
    end_timestamp: datetime
    custom_prompt: str = None

@app.get("/channels")
async def list_channels():
    """Get list of available Slack channels"""
    try:
        channels = get_available_channels(slack_client)
        if not channels:
            raise HTTPException(status_code=404, detail="No channels found")
        return {"channels": channels}
    except Exception as e:
        logging.error(f"Error fetching channels: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching channels: {str(e)}")

@app.post("/summarize")
async def create_summary(request: SummaryRequest):
    """Create a summary for a specific channel and time range"""
    try:
        # Validate timestamps
        if request.end_timestamp <= request.start_timestamp:
            raise HTTPException(
                status_code=400,
                detail="End timestamp must be after start timestamp"
            )

        # Convert datetime to Unix timestamps
        start_ts = request.start_timestamp.timestamp()
        end_ts = request.end_timestamp.timestamp()

        logging.info(f"Processing summary request for channel {request.channel_name} "
                    f"from {request.start_timestamp} to {request.end_timestamp}")

        # Get channel info first to validate channel exists
        try:
            channel_info = slack_client.conversations_info(channel=request.channel_name)
            if not channel_info["ok"]:
                raise HTTPException(
                    status_code=404,
                    detail=f"Channel '{request.channel_name}' not found or not accessible"
                )
        except Exception as e:
            raise HTTPException(
                status_code=404,
                detail=f"Error accessing channel: {str(e)}"
            )

        # Process the summary
        result = process_channel_summary(
            slack_client=slack_client,
            notion_client=notion_client,
            channel_name=request.channel_name,
            start_timestamp=start_ts,
            end_timestamp=end_ts,
            config=config,
            custom_prompt=request.custom_prompt
        )

        if not result:
            # Try to get message range information
            try:
                # Get latest message
                latest_message = slack_client.conversations_history(
                    channel=request.channel_name,
                    limit=1
                )
                
                # Get oldest message
                oldest_message = slack_client.conversations_history(
                    channel=request.channel_name,
                    limit=1,
                    oldest="0"
                )
                
                message_range = ""
                if latest_message["ok"] and latest_message.get("messages"):
                    latest_ts = float(latest_message["messages"][0].get("ts", 0))
                    latest_time = datetime.datetime.fromtimestamp(latest_ts)
                    message_range += f"Latest message: {latest_time.strftime('%Y-%m-%d %H:%M')}. "
                
                if oldest_message["ok"] and oldest_message.get("messages"):
                    oldest_ts = float(oldest_message["messages"][0].get("ts", 0))
                    oldest_time = datetime.datetime.fromtimestamp(oldest_ts)
                    message_range += f"Oldest message: {oldest_time.strftime('%Y-%m-%d %H:%M')}."
                
                if message_range:
                    raise HTTPException(
                        status_code=400,
                        detail=f"No messages found in the specified time range. {message_range}"
                    )
                else:
                    raise HTTPException(
                        status_code=400,
                        detail="No messages found in the specified time range. Channel might be empty."
                    )
            except Exception as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Failed to create summary: {str(e)}"
                )

        logging.info(f"Successfully created summary with page ID: {result}")
        return {"status": "success", "page_id": result}

    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error creating summary: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 