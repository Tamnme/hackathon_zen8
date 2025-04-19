DEFAULT_SUMMARY_PROMPT = """
Please analyze the following Slack conversation and create a comprehensive summary. 
Focus on the following aspects:

1. Key Discussion Points: What were the main topics discussed?
2. Decisions Made: Were any important decisions or conclusions reached?
3. Action Items: Were there any tasks assigned or action items identified?
4. Important Information: Were there any critical pieces of information shared?
5. Questions Raised: Were there any unanswered questions or topics that need follow-up?

Format the summary in a clear, structured way with appropriate headings and bullet points where needed.

Conversation:
{conversation}
"""

def get_summary_prompt(conversation: str, custom_prompt: str = None) -> str:
    """
    Get the prompt for the Gemini API.
    
    Args:
        conversation: The conversation text to summarize
        custom_prompt: Optional custom prompt template. If provided, it should contain {conversation} placeholder.
        
    Returns:
        The formatted prompt string
    """
    if custom_prompt:
        return custom_prompt.format(conversation=conversation)
    return DEFAULT_SUMMARY_PROMPT.format(conversation=conversation) 