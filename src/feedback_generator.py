import google.generativeai as genai

def generate_feedback(prompt, api_key):
    """Generate feedback using the Gemini model."""
    # Configure the API key
    genai.configure(api_key=api_key)
    
    # Initialize the model
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating feedback: {str(e)}")
        return "Unable to generate feedback at this time. Please try again later."
