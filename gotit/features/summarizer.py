import logging
import google.generativeai as genai
from .prompts import get_summary_prompt

def summarize_text_with_gemini(api_key: str, text: str, custom_prompt: str = None) -> str:
    """
    Summarize text using Google's Gemini API.
    
    Args:
        api_key: Gemini API key
        text: Text to summarize
        custom_prompt: Optional custom prompt template
        
    Returns:
        The generated summary
    """
    try:
        if not api_key:
            logging.error("No Gemini API key provided")
            return None
            
        if not text:
            logging.error("No text provided for summarization")
            return None

        # Configure the Gemini API
        genai.configure(api_key=api_key)
        
        # Get the model
        model = genai.GenerativeModel('gemini-pro')
        
        # Get the prompt
        prompt = get_summary_prompt(text, custom_prompt)
        logging.info(f"Generated prompt length: {len(prompt)} characters")
        
        # Generate the summary
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                top_p=0.8,
                top_k=40,
                max_output_tokens=2048,
            )
        )
        
        if not response:
            logging.error("No response received from Gemini API")
            return None
            
        if not response.text:
            logging.error("Empty response text from Gemini API")
            if hasattr(response, 'prompt_feedback'):
                logging.error(f"Prompt feedback: {response.prompt_feedback}")
            return None
            
        logging.info(f"Successfully generated summary of length: {len(response.text)} characters")
        return response.text
        
    except Exception as e:
        logging.error(f"Error generating summary with Gemini: {str(e)}")
        if hasattr(e, 'response'):
            logging.error(f"API Response: {e.response}")
        return None 