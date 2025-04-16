import logging
import google.generativeai as genai

def summarize_text_with_gemini(api_key: str, text_to_summarize: str, model: str = "gemini-pro") -> str | None:
    """
    Summarizes the given text using the Gemini API.

    Args:
        api_key: Your Gemini API key.
        text_to_summarize: The text content to summarize.
        model: The Gemini model to use for summarization.

    Returns:
        The summary text, or None if an error occurs.
    """
    if not text_to_summarize:
        logging.warning("No text provided to summarize.")
        return None

    logging.info(f"Sending text to Gemini for summarization using model {model}...")
    genai.configure(api_key=api_key)

    prompt = f"Please provide a concise summary of the following Slack conversation:\n\n{text_to_summarize}\n\nSummary:"

    try:
        model = genai.GenerativeModel(model)
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.5,
                max_output_tokens=250,
            )
        )
        
        if response and response.text:
            summary = response.text.strip()
            logging.info("Successfully received summary from Gemini.")
            return summary
        else:
            logging.error(f"Invalid response structure from Gemini: {response}")
            return None

    except Exception as e:
        logging.error(f"An unexpected error occurred during summarization: {e}")
        return None 