from google import genai
import os

api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

print("Testing Gemini 3.6 Flash...")

try:
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents="What is Python? Explain in simple language."
    )

    print("\nSUCCESS!\n")
    print(response.text)

except Exception as e:
    print("\nERROR:\n")
    print(e)