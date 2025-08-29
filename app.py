import os
from flask import Flask, render_template, request, redirect, url_for
from mistralai import Mistral
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Fetch API key securely from environment
api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    raise ValueError("❌ MISTRAL_API_KEY not found in .env file")
client = Mistral(api_key=api_key)

@app.route("/")
def index():
    return render_template("index.html")

# 🔹 Route to handle resume uploads
@app.route("/upload", methods=["POST"])
def upload():
    if "resume" not in request.files:
        return "No file uploaded", 400

    file = request.files["resume"]

    if file.filename == "":
        return "No selected file", 400

    # ✅ Save file temporarily
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    upload_path = os.path.join(upload_dir, file.filename)
    file.save(upload_path)

    # (Later: extract skills from the resume here)
    # For now, just pass a hardcoded skill
    return redirect(url_for("quiz_from_resume", skill="Python"))

# 🔹 Quiz route (called after resume upload or direct request)
@app.route("/quiz_from_resume")
def quiz_from_resume():
    skill = request.args.get("skill", "Python")  # fallback skill

    prompt = f"""
    Generate 5 multiple-choice quiz questions on {skill}.
    Format each question as:
    Q: <question>
    A. <option1>
    B. <option2>
    C. <option3>
    D. <option4>
    Answer: <correct option letter>
    """

    try:
        response = client.chat.complete(
            model="mistral-medium",
            messages=[{"role": "user", "content": prompt}]
        )
    except Exception as e:
        return f"❌ Error contacting Mistral API: {e}"

    # Extract response text
    try:
        quiz_text = response.choices[0].message["content"]
    except Exception:
        return "❌ Unexpected API response format"

    # Parse into questions
    questions = quiz_text.strip().split("Q:")[1:]
    quiz_data = []

    for q in questions:
        lines = [line for line in q.strip().split("\n") if line.strip()]
        if len(lines) < 6:  # Ensure question + 4 options + answer exist
            continue
        question = lines[0].strip()
        options = lines[1:5]
        answer = lines[-1].replace("Answer:", "").strip()
        quiz_data.append({"question": question, "options": options, "answer": answer})

    if not quiz_data:
        return "❌ No quiz data generated. Try again."

    return render_template("quiz.html", skill=skill, quiz_data=quiz_data)


if __name__ == "__main__":
    app.run(debug=True)