"""
Simple demo script for quick start with the Notion API.
"""
import os
from dotenv import load_dotenv
from notion_client import Client
from notion_client.errors import APIResponseError
from app.services.notion_client_manager import NotionManager
from datetime import datetime

def setup_env():
    """Set up environment variables and get required credentials"""
    # Load environment variables
    load_dotenv()
    api_key = os.getenv("NOTION_API_KEY")
    database_id = os.getenv("NOTION_DATABASE_ID")

    if not api_key:
        api_key = input("Enter your Notion API key: ")

    if not database_id:
        database_id = input("Enter your database ID: ")

    return api_key, database_id

def main():
    try:
        # Get credentials from environment
        api_key, database_id = setup_env()

        # Initialize the Notion manager
        notion = NotionManager(api_key)
        
        # Validate the connection before proceeding
        print("\nValidating connection to Notion API...")
        notion.validate_connection()
        print("Connection successful!")

        # Create a new database item with content
        page_title = "Quick Demo Page"
        page_content = """# Welcome to Notion API Demo
        
This is a demonstration of the Notion API integration with Python. Let me show you some basic Notion elements:

## Key Features
- ✅ Create pages and databases
- ✅ Add rich text content 
- ✅ Manage tasks and projects

### Task List:
- [ ] Learn Notion API basics
- [ ] Build a simple integration
- [ ] Test database operations
- [ ] Share with team members

Feel free to explore and customize this template for your needs!"""

        print(f"\nCreating database item with title: {page_title}")
        
        result = add_content_to_database(notion, database_id, datetime.now(), page_title, md_to_notion_blocks(page_content))
        
        if result["success"]:
            print("Database item created successfully!")
            print(f"Page URL: {result['page_url']}")
        else:
            print(f"Error creating database item: {result['error']}")

    except APIResponseError as e:
        if e.status == 500:
            print("\nError 500: Internal Server Error from Notion API. This usually indicates an issue with:")
            print("1. Your API key format (should start with 'secret_')")
            print("2. The parent page not being shared with your integration")
            print("\nPlease follow these steps:")
            print("1. Make sure your API key in .env starts with 'secret_'")
            print("2. Go to your Notion page (https://notion.so/")
            print(f"   Page ID: {parent_page_id.replace('-', '')}")
            print("3. Click '...' menu in the top right")
            print("4. Click 'Add connections'")
            print("5. Select your integration")
            print("\nAfter completing these steps, try running the script again.")
        elif e.code == "object_not_found":
            print("\nError: The page ID could not be found.")
            print("Make sure the parent page ID is correct and the page is accessible to your integration.")
        else:
            print(f"\nAPI Error: {e}")
            print("Status:", e.status)
            print("Code:", e.code)
    
    except ValueError as e:
        print(f"\nConfiguration Error: {e}")
        print("\nPlease check your API key and database ID.")
        
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
        
        page_url = f"https://notion.so/{new_page['id'].replace('-', '')}"
        
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
    
if __name__ == "__main__":
    main() 
