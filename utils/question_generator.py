import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_ENDPOINT = "https://api.mistral.ai/v1/chat/completions"


def parse_questions(raw_text):
    """
    Convert raw text from Mistral into a structured list of questions.
    """
    questions = []
    blocks = re.split(r"Q\d+\.", raw_text)  # split at Q1., Q2. etc.

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        lines = block.split("\n")
        question_text = lines[0].strip()  # first line = question

        options = []
        answer = None

        for line in lines[1:]:
            line = line.strip()
            if re.match(r"^[A-D]\.", line):     # keep the "A. Option" format
                options.append(line)
            elif line.startswith("Answer:"):
                answer = line.split("Answer:")[-1].strip().upper()

        if question_text and options and answer:
            questions.append({
                "question": question_text,
                "options": options,
                "answer": answer
            })

    return questions


def generate_questions(skill, max_retries=3):
    """
    Generates 5 MCQs for a given skill using Mistral API.
    Retries if 'Answer:' line is missing in the response.
    """
    prompt = f"""
You are an extremely careful and precise quiz generator.
Task: Generate exactly 5 multiple-choice questions (MCQs) on the topic: {skill}. {skill} can be any programming language, database, tool, or technology.

Requirements:

Each question must be factually accurate and relevant to {skill}.

Keep the difficulty level medium.

Include a code snippet only if directly relevant to the question. Otherwise, no code snippet.

If a code snippet is included, write it directly as plain text (no backticks, no quotes, no markdown, no comments).

Each question must have exactly 4 answer options labeled:
A.
B.
C.
D.

The correct answer must always be one of these 4 options. Do not use placeholders like "NONE OF THE ABOVE" or answers outside A-D.

Immediately after the options, include the correct answer using this exact format:
Answer: <A/B/C/D>

Ensure that questions do not repeat each time the generator runs. The 5 questions should be unique.

Do not include interactive prompts like “Your answer” or explanations.

Output format example (strictly follow this pattern for all 5 questions).

IMPORTANT: Generate a quiz with unique questions every time I run main.py. Do not repeat questions from previous runs. Each run should give me a new set of questions.

Add randomness so that the set of questions is different on every run, even if the skill is the same.

Include a variety of question types (e.g., definition, code explanation, best practices).

Even if the option is given in lower case, the correct answer must match the case used in the question.

For programming languages (Java, Python, C, C++, SQL), include some questions with code snippets to test user knowledge.

Code snippet–based questions must show valid, complete code fragments that compile/run correctly (no commented-out code, no syntax errors).

Please ensure snippets are short, clear, and directly tied to the question.

Always ensure factual accuracy of both questions and answers.

Question Format (strict):

Q1. [Question text]
[Optional code snippet if relevant]
A. [Option A]
B. [Option B]
C. [Option C]
D. [Option D]
Answer: [A/B/C/D]

Q2. [Question text]
[Optional code snippet if relevant]
A. [Option A]
B. [Option B]
C. [Option C]
D. [Option D]
Answer: [A/B/C/D]

Q3. [Question text]
[Optional code snippet if relevant]
A. [Option A]
B. [Option B]
C. [Option C]
D. [Option D]
Answer: [A/B/C/D]

Q4. [Question text]
[Optional code snippet if relevant]
A. [Option A]
B. [Option B]
C. [Option C]
D. [Option D]
Answer: [A/B/C/D]

Q5. [Question text]
[Optional code snippet if relevant]
A. [Option A]
B. [Option B]
C. [Option C]
D. [Option D]
Answer: [A/B/C/D]


Only output the questions and answers exactly as specified above. No extra text. Ensure 100% factual accuracy.
"""
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistral-tiny",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0
    }

    for attempt in range(max_retries):
        response = requests.post(MISTRAL_ENDPOINT, headers=headers, json=data)
        if response.status_code != 200:
            raise Exception(f"API error: {response.status_code} - {response.text}")

        content = response.json()["choices"][0]["message"]["content"]

        if "Answer:" in content:
            return parse_questions(content.strip())   # ✅ return structured list
        else:
            print(f"⚠️ Missing 'Answer:' line. Retrying ({attempt+1}/{max_retries})...")

    raise Exception("❌ Failed to generate questions with Answer line after multiple attempts.")



