import datetime
import logging
import argparse
from config.config import load_config
from features.slack_client import initialize_slack_client, get_slack_messages, get_available_channels, find_channel_by_name
from features.summarizer import summarize_text_with_gemini
from features.notion_client import initialize_notion_client, create_notion_page, send_summary_to_notion

def process_channel_summary(slack_client, notion_client, channel_name, start_timestamp, end_timestamp, config, custom_prompt=None):
    """
    Process a channel summary for a specific time range.
    
    Args:
        slack_client: Initialized Slack client
        notion_client: Initialized Notion client
        channel_name: Name of the channel to summarize
        start_timestamp: Start timestamp for messages
        end_timestamp: End timestamp for messages
        config: Configuration dictionary
        custom_prompt: Optional custom prompt template for Gemini
        
    Returns:
        The ID of the created Notion page
    """
    try:
        # Validate inputs
        if not channel_name:
            logging.error("No channel name provided")
            return None

        if not config.get('gemini', {}).get('api_key'):
            logging.error("No Gemini API key found in config")
            return None

        # Find channel by name
        channel_info = find_channel_by_name(slack_client, channel_name)
        if not channel_info:
            logging.error(f"Channel '{channel_name}' not found or not accessible")
            return None

        selected_channel_id = channel_info["id"]
        logging.info(f"Found channel: {channel_info['name']} (ID: {selected_channel_id})")

        # Fetch Slack messages
        messages_text_list = get_slack_messages(
            slack_client, 
            selected_channel_id, 
            start_timestamp, 
            end_timestamp
        )

        if not messages_text_list:
            logging.warning(f"No messages found for the specified time range in channel {channel_name}")
            return None

        logging.info(f"Found {len(messages_text_list)} messages to summarize")

        # Combine messages and summarize
        full_conversation = "\n".join(messages_text_list)
        logging.info(f"Combined conversation length: {len(full_conversation)} characters")

        summary = summarize_text_with_gemini(
            config['gemini']['api_key'], 
            full_conversation,
            custom_prompt
        )

        if not summary:
            logging.error("Failed to generate summary")
            return None

        logging.info("Successfully generated summary")

        # Create a new Notion page
        page_title = f"Slack Summary for #{channel_info['name']} ({datetime.datetime.fromtimestamp(start_timestamp).strftime('%Y-%m-%d %H:%M')} to {datetime.datetime.fromtimestamp(end_timestamp).strftime('%Y-%m-%d %H:%M')})"
        new_page_id = create_notion_page(notion_client, page_title)
        
        if not new_page_id:
            logging.error("Failed to create Notion page")
            return None

        logging.info(f"Created Notion page with ID: {new_page_id}")
        
        # Add the summary content to the new page
        send_summary_to_notion(
            notion_client,
            new_page_id,
            "Conversation Summary",
            summary
        )

        logging.info(f"Successfully created summary page with ID: {new_page_id}")
        return new_page_id

    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        return None

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Slack-Notion Summarizer')
    parser.add_argument('--channel', help='Name of the channel to summarize')
    parser.add_argument('--start', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end', help='End date (YYYY-MM-DD)')
    parser.add_argument('--api', action='store_true', help='Run as API server')
    args = parser.parse_args()

    logging.info("Starting Slack-Notion Summarizer script...")

    try:
        # Load configuration
        config = load_config()

        # Initialize clients
        slack_client = initialize_slack_client(config['slack']['bot_token'])
        notion_client = initialize_notion_client(config['notion']['api_key'])

        if args.api:
            # Import and run the API server
            from api import app
            import uvicorn
            uvicorn.run(app, host="0.0.0.0", port=8000)
            return

        # If running in CLI mode, use yesterday's date range if not specified
        if not args.start or not args.end:
            today = datetime.date.today()
            yesterday = today - datetime.timedelta(days=1)
            start_date = datetime.datetime.combine(yesterday, datetime.time.min)
            end_date = datetime.datetime.combine(yesterday, datetime.time.max)
        else:
            start_date = datetime.datetime.strptime(args.start, '%Y-%m-%d')
            end_date = datetime.datetime.strptime(args.end, '%Y-%m-%d')

        # Convert to Unix timestamps
        start_ts = start_date.timestamp()
        end_ts = end_date.timestamp()

        # Process the summary
        result = process_channel_summary(
            slack_client=slack_client,
            notion_client=notion_client,
            channel_name=args.channel,
            start_timestamp=start_ts,
            end_timestamp=end_ts,
            config=config
        )

        if not result:
            logging.error("Failed to create summary")
            return

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise

if __name__ == "__main__":
    main()

