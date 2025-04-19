import unittest
import sys
import os

# Add the function directly from simple_demo to avoid import dependencies
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

class TestMdToNotionBlocks(unittest.TestCase):
    
    def test_empty_string(self):
        """Test that an empty string returns an empty list of blocks."""
        md_content = ""
        expected = []
        actual = md_to_notion_blocks(md_content)
        self.assertEqual(actual, expected)
    
    def test_heading_conversion(self):
        """Test conversion of different heading levels."""
        md_content = "# Heading 1\n## Heading 2\n### Heading 3"
        actual = md_to_notion_blocks(md_content)
        
        expected = [
            {
                "object": "block",
                "type": "heading_1", 
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": "Heading 1"}}]
                }
            },
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "Heading 2"}}]
                }
            },
            {
                "object": "block", 
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": "Heading 3"}}]
                }
            }
        ]
        
        self.assertEqual(actual, expected)
    
    def test_list_conversion(self):
        """Test conversion of bulleted and numbered lists."""
        md_content = "- Bullet item\n1. Numbered item"
        actual = md_to_notion_blocks(md_content)
        
        expected = [
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": "Bullet item"}}]
                }
            },
            {
                "object": "block", 
                "type": "numbered_list_item",
                "numbered_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": "Numbered item"}}]
                }
            }
        ]
        
        self.assertEqual(actual, expected)
    
    def test_task_list_conversion(self):
        """Test conversion of task lists with checked and unchecked items."""
        md_content = "- [ ] Unchecked task\n- [x] Checked task"
        actual = md_to_notion_blocks(md_content)
        
        expected = [
            {
                "object": "block",
                "type": "to_do",
                "to_do": {
                    "rich_text": [{"type": "text", "text": {"content": "Unchecked task"}}],
                    "checked": False
                }
            },
            {
                "object": "block",
                "type": "to_do", 
                "to_do": {
                    "rich_text": [{"type": "text", "text": {"content": "Checked task"}}],
                    "checked": True
                }
            }
        ]
        
        self.assertEqual(actual, expected)
    
    def test_code_block_conversion(self):
        """Test conversion of code blocks."""
        md_content = "```python\nprint('Hello')"
        actual = md_to_notion_blocks(md_content)
        
        expected = [
            {
                "object": "block",
                "type": "code",
                "code": {
                    "rich_text": [{"type": "text", "text": {"content": "python"}}],
                    "language": "plain text"
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": "print('Hello')"}}]
                }
            }
        ]
        
        self.assertEqual(actual, expected)
    
    def test_quote_conversion(self):
        """Test conversion of quote blocks."""
        md_content = "> This is a quote"
        actual = md_to_notion_blocks(md_content)
        
        expected = [
            {
                "object": "block",
                "type": "quote",
                "quote": {
                    "rich_text": [{"type": "text", "text": {"content": "This is a quote"}}]
                }
            }
        ]
        
        self.assertEqual(actual, expected)
    
    def test_paragraph_conversion(self):
        """Test conversion of regular paragraph text."""
        md_content = "This is a normal paragraph."
        actual = md_to_notion_blocks(md_content)
        
        expected = [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": "This is a normal paragraph."}}]
                }
            }
        ]
        
        self.assertEqual(actual, expected)
    
    def test_mixed_content(self):
        """Test conversion of mixed content types."""
        md_content = """# Welcome to Notion
        
This is a paragraph.

## Features
- Bullet point 1
- [ ] Todo item
- [x] Completed item

> Important note"""
        
        actual = md_to_notion_blocks(md_content)
        
        # We should have 7 blocks in total
        self.assertEqual(len(actual), 7)
        
        # Check the types of each block
        self.assertEqual(actual[0]["type"], "heading_1")
        self.assertEqual(actual[1]["type"], "paragraph")
        self.assertEqual(actual[2]["type"], "heading_2")
        self.assertEqual(actual[3]["type"], "bulleted_list_item")
        self.assertEqual(actual[4]["type"], "to_do")
        self.assertEqual(actual[5]["type"], "to_do")
        self.assertEqual(actual[6]["type"], "quote")
        
        # Check content of first heading
        self.assertEqual(
            actual[0]["heading_1"]["rich_text"][0]["text"]["content"],
            "Welcome to Notion"
        )
        
        # Check that the todo items have correct checked status
        self.assertFalse(actual[4]["to_do"]["checked"])
        self.assertTrue(actual[5]["to_do"]["checked"])

if __name__ == "__main__":
    unittest.main() 