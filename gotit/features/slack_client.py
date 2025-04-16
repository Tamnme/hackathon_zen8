import datetime
import time
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from typing import List, Dict

def get_available_channels(slack_client: WebClient) -> List[Dict[str, str]]:
    """
    Fetches a list of available Slack channels that the bot has access to.

    Args:
        slack_client: Initialized Slack WebClient.

    Returns:
        A list of dictionaries containing channel information (id, name, topic, purpose).
    """
    try:
        # Get all channels the bot has access to
        response = slack_client.conversations_list(
            types="public_channel,private_channel",
            exclude_archived=True
        )

        if response["ok"]:
            channels = []
            for channel in response["channels"]:
                channel_info = {
                    "id": channel["id"],
                    "name": channel["name"],
                    "topic": channel.get("topic", {}).get("value", "No topic"),
                    "purpose": channel.get("purpose", {}).get("value", "No purpose")
                }
                channels.append(channel_info)
            
            logging.info(f"Found {len(channels)} available channels")
            return channels
        else:
            logging.error(f"Error fetching channels: {response.get('error')}")
            return []

    except SlackApiError as e:
        logging.error(f"Slack API Error fetching channels: {e.response['error']}")
        return []
    except Exception as e:
        logging.error(f"An unexpected error occurred fetching channels: {e}")
        return []

def get_slack_messages(slack_client: WebClient, channel_id: str, oldest_ts: float, latest_ts: float) -> list[str]:
    """
    Fetches messages from a Slack channel within a given timestamp range.

    Args:
        slack_client: Initialized Slack WebClient.
        channel_id: The ID of the channel to fetch messages from.
        oldest_ts: The start timestamp (Unix timestamp).
        latest_ts: The end timestamp (Unix timestamp).

    Returns:
        A list of message texts (user messages only).
    """
    messages = []
    cursor = None
    message_limit_per_page = 200  # Max allowed by Slack API is 1000, use lower for safety

    logging.info(f"Fetching messages from channel {channel_id} between {datetime.datetime.fromtimestamp(oldest_ts)} and {datetime.datetime.fromtimestamp(latest_ts)}")

    try:
        while True:
            response = slack_client.conversations_history(
                channel=channel_id,
                oldest=str(oldest_ts),
                latest=str(latest_ts),
                limit=message_limit_per_page,
                cursor=cursor
            )

            if response["ok"]:
                fetched_messages = response.get("messages", [])
                for msg in fetched_messages:
                    if msg.get("type") == "message" and msg.get("user") and msg.get("text"):
                        ts = datetime.datetime.fromtimestamp(float(msg.get('ts', 0))).strftime('%H:%M')
                        messages.append(f"[{ts}]: {msg['text']}")

                if response.get("has_more"):
                    cursor = response.get("response_metadata", {}).get("next_cursor")
                    logging.info("Fetching next page of messages...")
                    time.sleep(1)  # Respect rate limits
                else:
                    break
            else:
                logging.error(f"Error fetching Slack messages: {response.get('error')}")
                break

    except SlackApiError as e:
        logging.error(f"Slack API Error fetching history: {e.response['error']}")
    except Exception as e:
        logging.error(f"An unexpected error occurred fetching Slack messages: {e}")

    logging.info(f"Fetched {len(messages)} user messages.")
    return messages[::-1]  # Return messages in chronological order

def initialize_slack_client(token: str) -> WebClient:
    """
    Initialize and authenticate Slack client.
    
    Args:
        token: Slack bot token
        
    Returns:
        Initialized WebClient instance
        
    Raises:
        Exception: If client initialization or authentication fails
    """
    try:
        client = WebClient(token=token)
        client.auth_test()
        logging.info("Slack client initialized and authenticated.")
        return client
    except Exception as e:
        logging.error(f"Failed to initialize or authenticate Slack client: {e}")
        raise