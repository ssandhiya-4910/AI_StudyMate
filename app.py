from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY is missing from the .env file.")

client = OpenAI(api_key=api_key)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()

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
Use short headings and bullet points.
Keep the important information.

Study material:
{user_text}
""",

        "quiz": f"""
You are an AI study assistant for college students.

Create 5 useful multiple-choice questions from the following study material.
Give 4 options for each question and clearly show the correct answer.

Study material:
{user_text}
""",

        "explain": f"""
You are an AI study assistant for college students.

Explain the following topic in simple English.
Give:
1. Simple definition
2. Main points
3. One simple example

Topic:
{user_text}
""",

        "improve": f"""
You are an AI study assistant for college students.

Improve the following answer.
Make it clear, grammatically correct, and suitable for an exam.
Do not change the main meaning.

Original answer:
{user_text}
"""
    }

    prompt = prompts.get(task, prompts["explain"])

    try:
        response = client.responses.create(
            model="gpt-5.6-luna",
            input=prompt
        )

        return jsonify({
            "result": response.output_text
        })

    except Exception as e:
        return jsonify({
            "error": "Unable to get an AI response. Please try again."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)