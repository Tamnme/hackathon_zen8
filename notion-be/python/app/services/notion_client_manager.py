import os
import re
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
from notion_client import Client
from notion_client.errors import APIResponseError

class NotionManager:
    """
    A manager class for interacting with the Notion API.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Notion manager with API credentials.
        
        Args:
            api_key: Optional Notion API key. If not provided, it will be loaded from environment variable.
        """
        load_dotenv()
        self.api_key = api_key or os.getenv("NOTION_API_KEY")
        if not self.api_key:
            raise ValueError("Notion API key not found. Please provide it or set NOTION_API_KEY environment variable.")
        
    
        self.notion = Client(auth=self.api_key)

    def validate_connection(self) -> bool:
        """
        Validates that the API connection is working correctly.
        
        Returns:
            bool: True if connection is valid, raises an exception otherwise
        """
        try:
            # Try to list users, which is a lightweight API call
            self.notion.users.list()
            return True
        except APIResponseError as e:
            if e.code == "unauthorized":
                raise ValueError("Unauthorized: Your API key is invalid. Please check the key or generate a new one.")
            else:
                raise ValueError(f"API connection error: {str(e)}")

    def _format_page_id(self, page_id: str) -> str:
        """
        Format the page ID to ensure it's in the correct format for the Notion API.
        
        Args:
            page_id: The page ID to format
            
        Returns:
            The formatted page ID
        """
        # Remove any hyphens
        page_id = page_id.replace("-", "")
        
        # If the ID is already in UUID format, return it as is
        if re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', page_id):
            return page_id
            
        # Add hyphens in the UUID format if the ID is a plain string
        if len(page_id) == 32:
            return f"{page_id[0:8]}-{page_id[8:12]}-{page_id[12:16]}-{page_id[16:20]}-{page_id[20:32]}"
        
        return page_id
    
    def create_page(self, parent_page_id: str, title: str, content: str) -> Dict[str, Any]:
        """
        Create a new page in Notion with the given title and content.
        
        Args:
            parent_page_id: The ID of the parent page or database where this page will be created
            title: The title of the new page
            content: The content to add to the page
            
        Returns:
            The created page object
        """
        # Format the parent page ID
        formatted_page_id = self._format_page_id(parent_page_id)
        
        new_page = {
            "parent": {"page_id": formatted_page_id},
            "properties": {
                "title": {
                    "title": [
                        {
                            "text": {
                                "content": title
                            }
                        }
                    ]
                }
            },
            "children": [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": content
                                }
                            }
                        ]
                    }
                }
            ]
        }
        
        try:
            return self.notion.pages.create(**new_page)
        except APIResponseError as e:
            if "Make sure the relevant pages and databases are shared with your integration" in str(e):
                error_msg = (
                    f"Error: {e}\n\n"
                    f"Please make sure you've shared the page with your integration:\n"
                    f"1. Go to the Notion page with ID {formatted_page_id}\n"
                    f"2. Click the '...' menu in the top-right corner\n"
                    f"3. Click 'Add connections'\n"
                    f"4. Find and select your integration\n"
                )
                raise ValueError(error_msg) from e
            raise
    
    def create_database_item(self, database_id: str, properties: Dict[str, Any], content: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create a new item in a Notion database.
        
        Args:
            database_id: The ID of the database where to create the item
            properties: The properties for the new database item
            content: The content to add to the page
        Returns:
            The created database item
        """
        formatted_database_id = self._format_page_id(database_id)
        
        new_item = {
            "parent": {"database_id": formatted_database_id},
            "properties": properties,
            "children": content
        }
        
        try:
            return self.notion.pages.create(**new_item)
        except APIResponseError as e:
            if "Make sure the relevant pages and databases are shared with your integration" in str(e):
                error_msg = (
                    f"Error: {e}\n\n"
                    f"Please make sure you've shared the database with your integration:\n"
                    f"1. Go to the Notion database with ID {formatted_database_id}\n"
                    f"2. Click the '...' menu in the top-right corner\n"
                    f"3. Click 'Add connections'\n"
                    f"4. Find and select your integration\n"
                )
                raise ValueError(error_msg) from e
            raise
    
    def update_page(self, page_id: str, properties: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing page's properties.
        
        Args:
            page_id: The ID of the page to update
            properties: The properties to update
            
        Returns:
            The updated page object
        """
        formatted_page_id = self._format_page_id(page_id)
        return self.notion.pages.update(page_id=formatted_page_id, properties=properties)
    
    def append_blocks(self, page_id: str, blocks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Append blocks to an existing page.
        
        Args:
            page_id: The ID of the page to append blocks to
            blocks: List of block objects to append
            
        Returns:
            The response from the append operation
        """
        formatted_page_id = self._format_page_id(page_id)
        return self.notion.blocks.children.append(block_id=formatted_page_id, children=blocks)
    
    def create_text_block(self, content: str) -> Dict[str, Any]:
        """
        Create a paragraph block with text content.
        
        Args:
            content: The text content to add
            
        Returns:
            A block object that can be used with append_blocks
        """
        return {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": content
                        }
                    }
                ]
            }
        } 