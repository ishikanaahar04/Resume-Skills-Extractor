import csv
import docx2txt
import pytesseract
from PyPDF2 import PdfReader
from PIL import Image
import os

# Add path to tesseract executable if not in PATH (adjust if needed)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Skill database
SKILLS_DB = ["Python", "Java", "Machine Learning", "SQL", "C++", "HTML", "CSS", "JavaScript",
"Bootstrap", "Tailwind", "React", "Angular", "Vue.js", "Node.js", "Express.js", "Flask", "Django",
# Databases
"MySQL", "PostgreSQL", "MongoDB", "SQLite", "Firebase",
# Data Science & ML
"Pandas", "NumPy", "Matplotlib", "Seaborn", "Scikit-learn", "TensorFlow", "Keras", "PyTorch", "Data Analysis",
"Data Visualization", "Deep Learning", "Artificial Intelligence", "Natural Language Processing",
# Tools & Platforms
"Git", "Docker", "AWS", "Google Cloud", "Azure", "VS Code", "Jupyter", "Linux", "Power BI", "Tableau",
# Concepts
"OOP", "DSA", "REST API", "Microservices", "Agile", "CI/CD", "Unit Testing", "Cloud Computing",
# Soft Skills
"Communication", "Leadership", "Teamwork", "Problem Solving", "Time Management", "Creativity", "Critical Thinking"]

def extract_text_from_resume(file_path):
    if file_path.endswith('.pdf'):
        reader = PdfReader(file_path)
        return " ".join(page.extract_text() or "" for page in reader.pages)
    elif file_path.endswith('.docx'):
        return docx2txt.process(file_path)
    elif file_path.endswith(('.jpg', '.jpeg', '.png', '.tiff')):  # OCR for images
        image = Image.open(file_path)
        return pytesseract.image_to_string(image)
    else:
        raise ValueError("Unsupported file format")

import random

def extract_skills(text):
    text_lower = text.lower()
    found_skills = list(set([skill for skill in SKILLS_DB if skill.lower() in text_lower]))
    random.shuffle(found_skills)  # Randomize the order
    return found_skills


def extract_name(text):
    # Basic pattern to catch names: assumes name is in the first 5 lines and properly capitalized
    lines = text.strip().split("\n")
    for line in lines[:5]:
        words = line.strip().split()
        if 1 < len(words) <= 4 and all(w[0].isupper() for w in words if w.isalpha()):
            return " ".join(words)
    return "Unknown"

def save_to_csv(name, skills, output_file="extracted_resume_data.csv"):
    file_exists = os.path.isfile(output_file)
    with open(output_file, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["Name", "Skills"])
        writer.writerow([name, ", ".join(skills)])

if __name__ == "__main__":
    file_path = "C:\\Users\Ishika Nahar\Resume-Skills-Extractor\college_resume_ayush.pdf"

    try:
        text = extract_text_from_resume(file_path)
        skills = extract_skills(text)
        name = extract_name(text)

        print("Name:", name)
        print("Skills:", skills)

        save_to_csv(name, skills)

        print(f"Data saved to 'extracted_resume_data.csv' successfully.")

    except Exception as e:
        print("Error:", str(e))
