import os


def get_summarization_prompt(transcription_text: str) -> str:
    """
    Get the summarization prompt, either from environment variable or use default dummy prompt.
    
    Args:
        transcription_text: The transcription text to append to the prompt
        
    Returns:
        Complete prompt string with transcription text appended
    """
    # Check if custom prompt is set via environment variable
    custom_prompt = os.environ.get("SUMMARIZATION_PROMPT")
    
    if custom_prompt:
        # Use custom prompt from environment variable
        return f"{custom_prompt}\n{transcription_text}"
    else:
        # Use generic dummy prompt
        dummy_prompt = "Summarize this conversation with key points and structure it as follows:\n"
        dummy_prompt += "1. Conversation Summary: Provide an extended summary of the main discussion points\n"
        dummy_prompt += "2. Key Topics: Identify and discuss the main topics covered\n"
        dummy_prompt += "3. Important Details: Highlight any significant details or decisions made\n"
        dummy_prompt += "4. Overall Assessment: Provide a general assessment of the conversation\n"
        return f"{dummy_prompt}\n{transcription_text}"

