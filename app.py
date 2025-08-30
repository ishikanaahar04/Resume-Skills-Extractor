import os
from flask import Flask, render_template, request, redirect, url_for, session
from mistralai import Mistral
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = "aKFEMuDwJOvtphHDDOrh2qbfRP7jEA1L"  # Change to a secure key in production

# Fetch API key securely from environment
api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    raise ValueError("❌ MISTRAL_API_KEY not found in .env file")

client = Mistral(api_key=api_key)


@app.route("/")
def index():
    return render_template("index.html")


# 🔹 Upload resume
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

    # (Later: call your skill_extractor here)
    # For now → hardcode skill
    session["skill"] = "Python"
    return redirect(url_for("quiz_from_resume"))


# 🔹 Generate quiz from skill
@app.route("/quiz_from_resume")
def quiz_from_resume():
    skill = session.get("skill", "Python")

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

    # ✅ Extract response text safely
    try:
        quiz_text = response.choices[0].message["content"]
    except Exception:
        return "❌ Unexpected API response format"

    # Parse into structured quiz
    questions = quiz_text.strip().split("Q:")[1:]
    quiz_data = []

    for q in questions:
        lines = [line.strip() for line in q.strip().split("\n") if line.strip()]
        if len(lines) < 6:  # question + 4 options + answer
            continue

        question = lines[0]
        options = [opt.replace("A. ", "").replace("B. ", "").replace("C. ", "").replace("D. ", "")
                   for opt in lines[1:5]]
        answer = lines[-1].replace("Answer:", "").strip()

        quiz_data.append({"question": question, "options": options, "answer": answer})

    if not quiz_data:
        return "❌ No quiz data generated. Try again."

    # Store in session for navigation
    session["quiz_data"] = quiz_data
    session["score"] = 0
    session["current_q"] = 0
    session["skill"] = skill

    return redirect(url_for("question"))


# 🔹 Show one question at a time
@app.route("/question", methods=["GET", "POST"])
def question():
    if "quiz_data" not in session:
        return redirect(url_for("index"))

    quiz_data = session["quiz_data"]
    current_q = session["current_q"]

    if current_q >= len(quiz_data):
        return redirect(url_for("result"))

    question_data = quiz_data[current_q]

    if request.method == "POST":
        selected = request.form.get("answer")
        correct = question_data["answer"]

        if selected and selected.strip().upper() == correct.upper():
            session["score"] += 1

        session["current_q"] += 1
        return redirect(url_for("question"))

    return render_template(
        "question.html",
        q=question_data,
        q_index=current_q + 1,
        total=len(quiz_data),
        skill=session.get("skill", "Skill")
    )


# 🔹 Show result page
@app.route("/result")
def result():
    score = session.get("score", 0)
    total = len(session.get("quiz_data", []))
    skill = session.get("skill", "Skill")
    return render_template("result.html", score=score, total=total, skill=skill)


if __name__ == "__main__":
    app.run(debug=True)
