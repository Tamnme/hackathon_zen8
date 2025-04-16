import datetime
import logging
from config.config import load_config
from features.slack_client import initialize_slack_client, get_slack_messages, get_available_channels
from features.summarizer import summarize_text_with_gemini
from features.notion_client import initialize_notion_client, create_notion_page, send_summary_to_notion

def select_channel(channels):
    """
    Displays available channels and lets the user select one.
    
    Args:
        channels: List of channel dictionaries containing id, name, topic, and purpose
        
    Returns:
        The selected channel ID
    """
    print("\nAvailable Slack Channels:")
    print("-" * 80)
    print(f"{'#':<3} {'Channel Name':<20} {'Topic':<40} {'Purpose':<40}")
    print("-" * 80)
    
    for i, channel in enumerate(channels, 1):
        print(f"{i:<3} {channel['name']:<20} {channel['topic'][:40]:<40} {channel['purpose'][:40]:<40}")
    
    while True:
        try:
            choice = int(input("\nEnter the number of the channel to summarize: "))
            if 1 <= choice <= len(channels):
                return channels[choice - 1]['id']
            print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

def main():
    logging.info("Starting Slack-Notion Summarizer script...")

    try:
        # Load configuration
        config = load_config()

        # Initialize clients
        slack_client = initialize_slack_client(config['slack']['bot_token'])
        notion_client = initialize_notion_client(config['notion']['api_key'])

        # Get available channels and let user select one
        channels = get_available_channels(slack_client)
        if not channels:
            logging.error("No channels available or error fetching channels. Exiting.")
            return

        selected_channel_id = select_channel(channels)
        if not selected_channel_id:
            logging.error("No channel selected. Exiting.")
            return

        # Define time range (Yesterday)
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        start_of_yesterday = datetime.datetime.combine(yesterday, datetime.time.min)
        end_of_yesterday = datetime.datetime.combine(yesterday, datetime.time.max)

        # Convert to Unix timestamps for Slack API
        oldest_ts = start_of_yesterday.timestamp()
        latest_ts = end_of_yesterday.timestamp()

        # Fetch Slack messages
        messages_text_list = get_slack_messages(
            slack_client, 
            selected_channel_id, 
            oldest_ts, 
            latest_ts
        )

        if not messages_text_list:
            logging.warning(f"No user messages found for {yesterday.strftime('%Y-%m-%d')} in selected channel. Exiting.")
            return

        # Combine messages and summarize
        full_conversation = "\n".join(messages_text_list)
        summary = summarize_text_with_gemini(config['gemini']['api_key'], full_conversation)

        if not summary:
            logging.error("Failed to generate summary. Exiting.")
            return

        # Get channel name for the page title
        channel_info = slack_client.conversations_info(channel=selected_channel_id)
        channel_name = channel_info.get('channel', {}).get('name', 'UnknownChannel')
        
        # Create a new Notion page
        page_title = f"Slack Summary for {yesterday.strftime('%Y-%m-%d')} (#{channel_name})"
        new_page_id = create_notion_page(notion_client, page_title)
        
        # Add the summary content to the new page
        send_summary_to_notion(
            notion_client,
            new_page_id,
            "Conversation Summary",
            summary
        )

        logging.info(f"Script finished successfully. Created new Notion page with ID: {new_page_id}")

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise

if __name__ == "__main__":
    main()

