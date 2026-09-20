# AI StudyMate

AI StudyMate is an AI-powered student study assistant built using Flask and the OpenAI API.

## Features

- 📝 Summarize Notes
- ❓ Generate Quiz
- 💡 Explain Concepts
- ✍️ Improve Answers

## Technologies Used

- Python
- Flask
- HTML
- CSS
- JavaScript
- OpenAI API

## How It Works

1. Student enters study material, a topic, or an answer.
2. Student selects a study task.
3. The request is sent from the web interface to the Flask backend.
4. Flask sends a structured prompt to the AI model.
5. The AI-generated response is displayed on the webpage.

## Project Structure

```text
AI_StudyMate/
├── app.py
├── requirements.txt
├── .gitignore
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── script.js
