from utils.skill_extractor import extract_skills_from_csv
from utils.question_generator import generate_questions
from utils.quiz_runner import run_quiz

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")  # Can be used inside question_generator if needed

def main():
    csv_path = "extracted_resume_data.csv"  # Your CSV with extracted names and skills
    users = extract_skills_from_csv(csv_path)

    for name, skills in users:
        print(f"\n👋 Welcome {name}!")
        print(f"📘 Skills selected for quiz: {', '.join(skills)}")

        total_score = 0
        max_score = 0

        for skill in skills:
            print(f"\n🎯 Skill: {skill}\n")
            try:
                questions = generate_questions(skill)  # ✅ Corrected: only one argument
                score = run_quiz(questions)
                total_score += score
                max_score += 5
            except Exception as e:
                print(f"⚠️ Error generating questions for {skill}: {e}")

        print(f"\n📝 Final Score for {name}: {total_score} / {max_score}")
        print("=" * 50)

if __name__ == "__main__":
    main()
