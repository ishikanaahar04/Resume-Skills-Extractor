import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_ENDPOINT = "https://api.mistral.ai/v1/chat/completions"

def generate_questions(skill):
    prompt = f"""
You are an extremely careful and precise quiz generator.

Generate exactly 5 multiple-choice questions (MCQs) on the topic: {skill}.

Each question must meet these requirements:

- A clear and factually accurate question statement.
- Exactly 4 answer options labeled A, B, C, and D.
- One and only one correct answer.
- The correct answer must be clearly and accurately indicated on a separate line as:
  Answer: <Correct Option Letter>
- The correct answer letter must **match the option text**.
- All answers must be verified and authentic — no guesses or approximations.
- Avoid any mismatches between answer letters and texts.
- Do not include ambiguous, tricky, or misleading questions.
- Strictly follow the format shown below with no additional explanation or filler:

Q1. [Question text]
A. [Option A]
B. [Option B]
C. [Option C]
D. [Option D]
Answer: [A/B/C/D]

Q2. ...

Only output the questions and answers exactly as specified above.

No additional text, corrections, labels, or instructions.

Ensure 100% factual and formatting accuracy.
"""




    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistral-tiny",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0  # Lower temperature for more deterministic output
    }

    response = requests.post(MISTRAL_ENDPOINT, headers=headers, json=data)

    if response.status_code != 200:
        raise Exception(f"API error: {response.status_code} - {response.text}")

    content = response.json()["choices"][0]["message"]["content"]
    return content.strip()
