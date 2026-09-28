from flask import Flask, render_template, request, jsonify
from google import genai
import os

app = Flask(__name__)

# Get Gemini API key from Render
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not configured.")

# Create Gemini client
client = genai.Client(api_key=api_key)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Invalid request."
        }), 400

    user_text = data.get("text", "").strip()
    task = data.get("task", "explain")

    if not user_text:
        return jsonify({
            "error": "Please enter some text first."
        }), 400

    prompts = {
        "summarize": f"""
You are an AI study assistant for college students.

Summarize the following study material in simple English.

Use:
- A clear heading
- Short bullet points
- Important information
- Easy-to-understand language

Study material:
{user_text}
""",

        "quiz": f"""
You are an AI study assistant for college students.

Create 5 useful multiple-choice questions from the following study material.

For each question:
- Write the question
- Give four options: A, B, C and D
- Clearly identify the correct answer

Study material:
{user_text}
""",

        "explain": f"""
You are an AI study assistant for college students.

Explain the following topic in simple English.

Use this format:

1. Simple Definition
2. Main Points
3. Simple Example

Topic:
{user_text}
""",

        "improve": f"""
You are an AI study assistant for college students.

Improve the following answer.

Requirements:
- Correct grammar
- Make it clear
- Make it suitable for an exam
- Keep the original meaning
- Do not add unrelated information

Original answer:
{user_text}
"""
    }

    prompt = prompts.get(task, prompts["explain"])

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        result = response.text

        if not result:
            return jsonify({
                "error": "No response was generated."
            }), 500

        return jsonify({
            "result": result
        })

    except Exception:
        return jsonify({
            "error": "Unable to get an AI response. Please try again."
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
