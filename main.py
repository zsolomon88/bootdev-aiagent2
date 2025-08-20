import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()   
# Access the environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

from google import genai

# Initialize the Gemini client with the API key
client = genai.Client(api_key=GEMINI_API_KEY)


def main():
    if(len(sys.argv) < 2):
        print("Please provide a prompt as a command line argument.")
        exit(1)
    verbose = False
    if "--verbose" in sys.argv:
        verbose = True
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=sys.argv[1],
       )
        print(response.text)
        if verbose:
            print(f"User prompt: {sys.argv[1]}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
