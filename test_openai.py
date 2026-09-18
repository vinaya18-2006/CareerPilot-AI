from dotenv import load_dotenv
import os

from openai import OpenAI


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("❌ API key not found")
    exit()


client = OpenAI(
    api_key=api_key
)


response = client.responses.create(
    model="gpt-4o-mini",
    input="Say 'CareerPilot AI is connected!'"
)


print(response.output_text)