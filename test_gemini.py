from google import genai
import os

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("❌ GEMINI_API_KEY is not set.")
    exit()

client = genai.Client(api_key=api_key)

print("\nAvailable Gemini models:\n")

try:
    for model in client.models.list():
        print(model.name)

except Exception as e:
    print("\n❌ ERROR:")
    print(e)