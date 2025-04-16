import logging
from notion_client import Client as NotionClient
from notion_client.errors import APIResponseError
from datetime import datetime

def initialize_notion_client(auth_token: str) -> NotionClient:
    """
    Initialize and authenticate Notion client.
    
    Args:
        auth_token: Notion API token
        
    Returns:
        Initialized NotionClient instance
        
    Raises:
        Exception: If client initialization or authentication fails
    """
    try:
        client = NotionClient(auth=auth_token)
        logging.info("Notion client initialized.")
        return client
    except Exception as e:
        logging.error(f"Failed to initialize Notion client: {e}")
        raise

def create_notion_page(notion_client: NotionClient, title: str, parent_database_id: str = None) -> str:
    """
    Creates a new Notion page.

    Args:
        notion_client: Initialized Notion Client.
        title: The title for the new page.
        parent_database_id: Optional ID of the parent database. If not provided, creates a top-level page.

    Returns:
        The ID of the created page.

    Raises:
        Exception: If page creation fails
    """
    try:
        # Prepare the page properties
        properties = {
            "title": {
                "title": [
                    {
                        "text": {
                            "content": title
                        }
                    }
                ]
            }
        }

        # If parent_database_id is provided, use it as the parent
        if parent_database_id:
            parent = {
                "database_id": parent_database_id
            }
        else:
            # Create a top-level page
            parent = {
                "type": "workspace",
                "workspace": True
            }

        # Create the page
        response = notion_client.pages.create(
            parent=parent,
            properties=properties
        )

        page_id = response["id"]
        logging.info(f"Successfully created Notion page with ID: {page_id}")
        return page_id

    except APIResponseError as e:
        logging.error(f"Notion API Error creating page: {e.body}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred creating Notion page: {e}")
        raise

def send_summary_to_notion(notion_client: NotionClient, page_id: str, title: str, summary_text: str):
    """
    Appends the summary text as new blocks to a Notion page.

    Args:
        notion_client: Initialized Notion Client.
        page_id: The ID of the Notion page to append content to.
        title: The title for the summary section (e.g., "Summary for YYYY-MM-DD").
        summary_text: The summary content.
    """
    logging.info(f"Sending summary to Notion page ID: {page_id}")

    summary_paragraphs = summary_text.strip().split('\n')
    blocks_to_append = [
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": title}}]
            }
        }
    ]
    
    for paragraph in summary_paragraphs:
        if paragraph:  # Avoid empty blocks
            blocks_to_append.append(
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": paragraph}}]
                    }
                }
            )
    
    # Add a divider for separation
    blocks_to_append.append({"object": "block", "type": "divider", "divider": {}})

    try:
        notion_client.blocks.children.append(
            block_id=page_id,
            children=blocks_to_append
        )
        logging.info("Successfully appended summary to Notion page.")
    except APIResponseError as e:
        logging.error(f"Notion API Error: {e.body}")
    except Exception as e:
        logging.error(f"An unexpected error occurred sending to Notion: {e}") 