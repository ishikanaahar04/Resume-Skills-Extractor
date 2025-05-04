import re
import docx2txt
from PyPDF2 import PdfReader

# List of skills to search for in the resume
SKILLS_DB = ["Python", "Java", "Machine Learning", "SQL", "HTML", "CSS", "JavaScript",
"HTML", "CSS", "Bootstrap", "Tailwind", "React", "Angular", "Vue.js", "Node.js", "Express.js", "Flask", "Django",
# Databases
"SQL", "MySQL", "PostgreSQL", "MongoDB", "SQLite", "Firebase",
# Data Science & ML

"Pandas", "NumPy", "Matplotlib", "Seaborn", "Scikit-learn", "TensorFlow", "Keras", "PyTorch", "Data Analysis",
"Data Visualization", "Machine Learning", "Deep Learning", "Artificial Intelligence", "Natural Language Processing",

# Tools & Platforms
"Git", "GitHub", "Docker", "AWS", "Google Cloud", "Azure", "Jira", "VS Code", "Jupyter", "Linux", "Power BI", "Tableau",
# Concepts
"OOP", "DSA", "REST API", "Microservices", "Agile", "CI/CD", "Unit Testing", "Cloud Computing",
# Soft Skills
"Communication", "Leadership", "Teamwork", "Problem Solving", "Time Management", "Creativity", "Critical Thinking"]

def extract_text_from_resume(file_path):
    """
    Extracts text from a resume file (PDF or DOCX).
    Args:
    - file_path (str): Path to the resume file.
    
    Returns:
    - str: Extracted text from the resume.
    """
    if file_path.endswith('.pdf'):
        reader = PdfReader(file_path)
        return " ".join(page.extract_text() for page in reader.pages)
    elif file_path.endswith('.docx'):
        return docx2txt.process(file_path)
    else:
        raise ValueError("Unsupported file type")

def extract_skills(text):
    """
    Extracts the skills from the resume text based on the predefined skills database.
    Args:
    - text (str): Extracted text from the resume.
    
    Returns:
    - list: A list of found skills from the resume.
    """
    text = text.lower()  # Make text lowercase for case-insensitive matching
    found_skills = [skill for skill in SKILLS_DB if skill.lower() in text]
    return found_skills

# Example of usage:
file_path = 'college_resume_ayush.pdf'  # Replace with the actual file path

# Extract text from the resume file
resume_text = extract_text_from_resume(file_path)

# Extract skills from the resume text
skills = extract_skills(resume_text)

# Print the extracted skills
print("Extracted Skills:", skills)