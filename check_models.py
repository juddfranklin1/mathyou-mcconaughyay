from dotenv import load_dotenv
load_dotenv()
import os
import google.generativeai as genai

api_key = os.environ.get('GEMINI_API_KEY')
if not api_key:
    print("No API key found in environment variables.")
else:
    genai.configure(api_key=api_key)
    print("Listing available models for your API key...")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")
    except Exception as e:
        print(f"Error listing models: {e}")