"""
Simple demo script for quick start with the Notion API.
"""
import os
from dotenv import load_dotenv
from notion_client import Client
from notion_client.errors import APIResponseError
from app.services.notion_client_manager import NotionManager
from datetime import datetime

def create_notion_summary(api_key: str, database_id: str, page_title: str, page_content: str, time: datetime):        # Get credentials from environment
    # Initialize the Notion manager
    notion = NotionManager(api_key)
    
    # Validate the connection before proceeding
    print("\nValidating connection to Notion API...")
    notion.validate_connection()
    print("Connection successful!")
    result = add_content_to_database(notion, database_id, time, page_title, md_to_notion_blocks(page_content))
    return result
        
def add_content_to_database(notion:NotionManager, database_id: str, time: datetime, title: str, content: str):
    try:
        # Validate connection first
        if not notion.validate_connection():
            return {
                "success": False,
                "error": "Could not validate connection to Notion API",
                "page_url": None
            }
            
        # Create properties for database item
        properties = {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": title
                        }
                    }
                ]
            },
            "Created": {
                "date": {
                    "start": time.strftime("%Y-%m-%d %H:%M:%S")
                }
            }
        }
            
        # Create the database item
        new_page = notion.create_database_item(database_id, properties, content)
        
        page_url = new_page.get('url')
        
        return {
            "success": True,
            "error": None,
            "page_url": page_url
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "page_url": None
        }

def md_to_notion_blocks(md_content: str) -> list:
    """
    Convert markdown content to Notion blocks format.
    
    Args:
        md_content: Markdown formatted string
        
    Returns:
        List of Notion block objects
    """
    blocks = []
    lines = md_content.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Headers
        if line.startswith('# '):
            blocks.append({
                "object": "block",
                "type": "heading_1", 
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": line[2:]}}]
                }
            })
        elif line.startswith('## '):
            blocks.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": line[3:]}}]
                }
            })
        elif line.startswith('### '):
            blocks.append({
                "object": "block", 
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": line[4:]}}]
                }
            })
            
        # Task Lists - check these before other lists
        elif line.startswith("- [ ]"):
            blocks.append({
                "object": "block",
                "type": "to_do",
                "to_do": {
                    "rich_text": [{"type": "text", "text": {"content": line[5:].strip()}}],
                    "checked": False
                }
            })
        elif line.startswith("- [x]") or line.startswith("- [X]"):
            blocks.append({
                "object": "block",
                "type": "to_do", 
                "to_do": {
                    "rich_text": [{"type": "text", "text": {"content": line[5:].strip()}}],
                    "checked": True
                }
            })
            
        # Lists - check these after task lists    
        elif line.startswith('- '):
            blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": line[2:]}}]
                }
            })
        elif line.startswith('1. '):
            blocks.append({
                "object": "block", 
                "type": "numbered_list_item",
                "numbered_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": line[3:]}}]
                }
            })
            
        # Code Blocks
        elif line.startswith('```'):
            blocks.append({
                "object": "block",
                "type": "code",
                "code": {
                    "rich_text": [{"type": "text", "text": {"content": line[3:]}}],
                    "language": "plain text"
                }
            })
            
        # Quotes
        elif line.startswith('>'):
            blocks.append({
                "object": "block",
                "type": "quote",
                "quote": {
                    "rich_text": [{"type": "text", "text": {"content": line[2:]}}]
                }
            })
            
        # Default to Paragraph
        else:
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": line}}]
                }
            })
            
    return blocks