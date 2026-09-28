from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

app = Flask(__name__)

# Get OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY is not configured.")

# Create OpenAI client
client = OpenAI(api_key=api_key)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    try:
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

Requirements:
- Use a short heading
- Use clear bullet points
- Keep important information
- Make it easy for students to study

Study material:
{user_text}
""",

            "quiz": f"""
You are an AI study assistant for college students.

Create 5 useful multiple-choice questions from the following study material.

For each question:
- Give the question
- Give 4 options: A, B, C, D
- Clearly mention the correct answer

Study material:
{user_text}
""",

            "explain": f"""
You are an AI study assistant for college students.

Explain the following topic in simple English.

Give the answer in this format:

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
- Make the answer clear
- Make it suitable for an exam
- Keep the original meaning
- Do not add unrelated information

Original answer:
{user_text}
"""
        }

        prompt = prompts.get(task, prompts["explain"])

        response = client.responses.create(
            model="gpt-5.6-luna",
            input=prompt
        )

        result = response.output_text

        return jsonify({
            "result": result
        })

    except Exception:
        return jsonify({
            "error": "Unable to get an AI response. Please try again."
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
