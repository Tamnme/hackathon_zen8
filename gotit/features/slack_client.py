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
        # First, verify the bot's authentication
        auth_test = slack_client.auth_test()
        if not auth_test["ok"]:
            logging.error(f"Authentication failed: {auth_test.get('error')}")
            return []

        # Get all channels the bot has access to
        response = slack_client.conversations_list(
            types="public_channel,private_channel",
            exclude_archived=True,
            limit=1000  # Maximum allowed by Slack API
        )

        if response["ok"]:
            channels = []
            channel_names = []
            for channel in response["channels"]:
                channel_info = {
                    "id": channel["id"],
                    "name": channel["name"],
                    "topic": channel.get("topic", {}).get("value", "No topic"),
                    "purpose": channel.get("purpose", {}).get("value", "No purpose"),
                    "is_private": channel.get("is_private", False),
                    "num_members": channel.get("num_members", 0)
                }
                channels.append(channel_info)
                channel_names.append(channel["name"])
            
            # Log all channel names
            logging.info("Available channels:")
            for name in sorted(channel_names):
                logging.info(f"  - {name}")
            
            logging.info(f"Total channels found: {len(channels)}")
            return channels
        else:
            error = response.get('error', 'Unknown error')
            logging.error(f"Error fetching channels: {error}")
            return []

    except SlackApiError as e:
        logging.error(f"Slack API Error fetching channels: {e.response['error']}")
        return []
    except Exception as e:
        logging.error(f"An unexpected error occurred fetching channels: {str(e)}")
        return []

def find_channel_by_name(slack_client: WebClient, channel_name: str) -> Dict[str, str]:
    """
    Find a channel by its name, with improved error handling and logging.
    
    Args:
        slack_client: Initialized Slack WebClient
        channel_name: Name of the channel to find
        
    Returns:
        Channel information dictionary if found, None otherwise
    """
    try:
        # First try direct lookup
        try:
            response = slack_client.conversations_info(channel=channel_name)
            if response["ok"]:
                channel = response["channel"]
                return {
                    "id": channel["id"],
                    "name": channel["name"],
                    "topic": channel.get("topic", {}).get("value", "No topic"),
                    "purpose": channel.get("purpose", {}).get("value", "No purpose"),
                    "is_private": channel.get("is_private", False),
                    "num_members": channel.get("num_members", 0)
                }
        except SlackApiError as e:
            if e.response["error"] != "channel_not_found":
                logging.error(f"Error looking up channel: {e.response['error']}")
                return None

        # If direct lookup fails, try searching in available channels
        channels = get_available_channels(slack_client)
        if not channels:
            logging.error("No channels available to search")
            return None

        # Try exact match first
        for channel in channels:
            if channel["name"].lower() == channel_name.lower():
                logging.info(f"Found channel by exact match: {channel['name']}")
                return channel

        # Try partial match
        matching_channels = []
        for channel in channels:
            if channel_name.lower() in channel["name"].lower():
                matching_channels.append(channel)

        if matching_channels:
            logging.info(f"Found {len(matching_channels)} channels with similar names")
            return matching_channels[0]  # Return the first match

        logging.error(f"Channel '{channel_name}' not found")
        return None

    except Exception as e:
        logging.error(f"Error finding channel: {str(e)}")
        return None

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
        # First, get channel info for better logging
        channel_info = slack_client.conversations_info(channel=channel_id)
        channel_name = channel_info.get('channel', {}).get('name', 'UnknownChannel')
        logging.info(f"Channel name: {channel_name}")

        # Try to get the latest message timestamp in the channel
        latest_message = slack_client.conversations_history(
            channel=channel_id,
            limit=1
        )
        
        if latest_message["ok"] and latest_message.get("messages"):
            latest_message_ts = float(latest_message["messages"][0].get("ts", 0))
            latest_message_time = datetime.datetime.fromtimestamp(latest_message_ts)
            logging.info(f"Latest message in channel: {latest_message_time}")

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

    if not messages:
        # Try to get the first message in the channel to provide more context
        try:
            first_message = slack_client.conversations_history(
                channel=channel_id,
                limit=1,
                oldest="0"  # Get the oldest message
            )
            if first_message["ok"] and first_message.get("messages"):
                first_message_ts = float(first_message["messages"][0].get("ts", 0))
                first_message_time = datetime.datetime.fromtimestamp(first_message_ts)
                logging.info(f"First message in channel: {first_message_time}")
        except Exception as e:
            logging.error(f"Error fetching first message: {e}")

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