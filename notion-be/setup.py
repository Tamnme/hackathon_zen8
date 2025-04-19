"""
Setup script to help users configure their Notion integration.
"""
import os
import sys
import re
import webbrowser
from pathlib import Path

def main():
    print("\n========== Notion API Setup ==========\n")
    print("This script will help you set up your Notion integration.")
    print("You will need to:\n")
    print("1. Create a Notion integration to get an API key")
    print("2. Share a Notion page with your integration")
    print("3. Store these credentials in a .env file\n")
    
    # Check for existing .env file
    env_path = Path('.env')
    env_exists = env_path.exists()
    
    if env_exists:
        print("Found existing .env file. Do you want to update it?")
        choice = input("Enter 'y' to update or 'n' to exit: ").lower()
        if choice != 'y':
            print("Exiting setup.")
            return
    
    # Get Notion API key
    print("\n----- Step 1: Notion API Key -----\n")
    print("You need to create a Notion integration to get an API key.")
    print("Opening Notion integration page in your browser...")
    
    try:
        webbrowser.open("https://www.notion.so/my-integrations")
    except:
        print("Could not open browser automatically.")
    
    print("\nInstructions:")
    print("1. Click 'New integration'")
    print("2. Give it a name (e.g., 'Python Notion Integration')")
    print("3. Select a workspace where you want to use it")
    print("4. Click 'Submit'")
    print("5. Copy the 'Internal Integration Secret' (starts with 'secret_')")
    
    api_key = input("\nPaste your Notion API key here: ").strip()
    
    # Validate API key format
    if not api_key.startswith("secret_"):
        print("\nWarning: Your API key should start with 'secret_'.")
        print("Make sure you're using the correct key.")
        confirm = input("Continue anyway? (y/n): ").lower()
        if confirm != 'y':
            print("Exiting setup.")
            return
    
    # Get page ID
    print("\n----- Step 2: Notion Page ID -----\n")
    print("Now you need to share a Notion page with your integration.")
    print("Instructions:")
    print("1. Open the Notion page where you want to add content")
    print("2. Copy the page URL from your browser")
    
    page_url = input("\nPaste your Notion page URL here: ").strip()
    
    # Extract page ID from URL
    page_id = None
    
    # Try to extract page ID from URL
    url_pattern = r'https?://(?:www\.)?notion\.so/(?:[^/]+/)?(?:[^-]+)-([a-f0-9]+)'
    url_match = re.search(url_pattern, page_url)
    
    if url_match:
        page_id = url_match.group(1)
    else:
        # Ask for manual entry
        print("\nCould not extract page ID from URL.")
        print("The page ID is usually the last part of the URL, after the last hyphen.")
        page_id = input("Please enter the page ID manually: ").strip()
    
    # Remind user to share the page with the integration
    print("\n----- Step 3: Share Page with Integration -----\n")
    print("You need to share your Notion page with your integration:")
    print("1. Go back to your Notion page")
    print("2. Click the '...' menu in the top-right corner")
    print("3. Click 'Add connections'")
    print("4. Find and select your integration")
    
    input("\nPress Enter once you've shared the page with your integration... ")
    
    # Save to .env file
    print("\n----- Saving Configuration -----\n")
    
    with open('.env', 'w') as f:
        f.write("# Notion API key\n")
        f.write(f"NOTION_API_KEY={api_key}\n\n")
        f.write("# Parent page ID where new pages will be created\n")
        f.write(f"NOTION_PARENT_PAGE_ID={page_id}\n")
    
    print("Configuration saved to .env file.")
    print("\n----- Setup Complete -----\n")
    print("You can now run the example scripts:")
    print("- python simple_demo.py (interactive demo)")
    print("- python example.py (automated example)")
    
    # Ask if they want to run the simple demo
    run_demo = input("\nWould you like to run the simple demo now? (y/n): ").lower()
    if run_demo == 'y':
        print("\nRunning simple_demo.py...")
        print("----------------------------\n")
        # Import and run instead of using subprocess to maintain the Python environment
        try:
            sys.path.insert(0, os.getcwd())
            from python.app.services.add_content_to_database import main as run_demo
            run_demo()
        except Exception as e:
            print(f"Error running demo: {e}")

if __name__ == "__main__":
    main() 