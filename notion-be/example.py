import os
from python.app.services.notion_client_manager import NotionManager
from dotenv import load_dotenv

def main():
    """
    Main function to demonstrate Notion API usage.
    """
    # Load environment variables
    load_dotenv()
    
    # Initialize the Notion manager
    try:
        notion = NotionManager()
        
        # Get parent page ID from environment variable or input
        parent_page_id = os.getenv("NOTION_PARENT_PAGE_ID")
        if not parent_page_id:
            parent_page_id = input("Enter the parent page ID: ")
        
        # Create a new page
        title = "Sample Page from Python"
        content = "This is a page created using the Notion API from Python."
        
        print(f"Creating a new page titled: {title}")
        new_page = notion.create_page(parent_page_id, title, content)
        
        print(f"New page created with ID: {new_page['id']}")
        
        # Append additional content to the page
        print("Appending additional content to the page...")
        additional_blocks = [
            notion.create_text_block("This is additional text added to the page."),
            notion.create_text_block("The NotionManager makes it easy to interact with the Notion API.")
        ]
        
        notion.append_blocks(new_page['id'], additional_blocks)
        print("Additional content appended successfully!")
        
        # Update the page title
        print("Updating the page title...")
        updated_properties = {
            "title": {
                "title": [
                    {
                        "text": {
                            "content": "Updated Page Title"
                        }
                    }
                ]
            }
        }
        
        notion.update_page(new_page['id'], updated_properties)
        print("Page title updated successfully!")
        
        print("\nExample completed! Check your Notion workspace to see the changes.")
        print(f"Page URL: https://notion.so/{new_page['id'].replace('-', '')}")
        
    except ValueError as e:
        print(f"\nError: {e}")
        print("\nIf you haven't set up your Notion credentials yet, try running:")
        print("python setup.py")

if __name__ == "__main__":
    main() 