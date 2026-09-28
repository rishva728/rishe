from flask import Flask, render_template, request, jsonify
from google import genai
import os
import time

app = Flask(__name__)

# ==============================
# Gemini API Configuration
# ==============================

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("WARNING: GEMINI_API_KEY is not set.")
    client = None
else:
    client = genai.Client(api_key=api_key)


# ==============================
# Home Page
# ==============================

@app.route("/")
def home():
    return render_template("index.html")


# ==============================
# Ask EduGenie
# ==============================

@app.route("/ask", methods=["POST"])
def ask():

    data = request.get_json()

    if not data:
        return jsonify({
            "answer": "Please enter a question."
        })

    question = data.get("question", "").strip()

    if not question:
        return jsonify({
            "answer": "Please enter a question."
        })

    if client is None:
        return jsonify({
            "answer": "Gemini API key is not configured."
        })

    prompt = f"""
You are EduGenie, a helpful AI learning assistant for college students.

Your job is to help students understand their subjects clearly.

Instructions:
- Explain in simple and easy language.
- Give examples when useful.
- Use bullet points when appropriate.
- Avoid unnecessarily complicated words.
- If the student asks a programming question, provide a simple example.
- Be friendly and educational.

Student question:
{question}
"""

    # ==============================
    # Gemini API
    # ==============================

    for attempt in range(3):

        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            answer = response.text

            if not answer:
                answer = "Sorry, I couldn't generate an answer."

            return jsonify({
                "answer": answer
            })

        except Exception as e:

            error_text = str(e)

            print(
                f"GEMINI ERROR "
                f"(Attempt {attempt + 1}/3): {error_text}"
            )

            # Retry temporary errors
            if "503" in error_text or "UNAVAILABLE" in error_text:

                if attempt < 2:
                    time.sleep(2)
                    continue

                return jsonify({
                    "answer": "Gemini is temporarily busy. Please try again."
                })

            # Other errors
            return jsonify({
                "answer": f"Gemini error: {error_text}"
            })

    return jsonify({
        "answer": "Something went wrong. Please try again."
    })


# ==============================
# Run Flask App
# ==============================

if __name__ == "__main__":
    app.run(debug=True)