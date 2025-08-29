import pandas as pd

def extract_skills_from_csv(csv_path, top_n=5):
    """
    Extract latest skills for each user from CSV.
    By default, only the first top_n skills are returned (default 5).
    """
    df = pd.read_csv(csv_path)

    # Ensure required columns exist
    if not {'Name', 'Skills'}.issubset(df.columns):
        raise ValueError("CSV must contain 'Name' and 'Skills' columns")

    latest_skills = {}

    for _, row in df.iterrows():
        name = str(row['Name']).strip()
        skills_str = row['Skills']
        
        if pd.isna(skills_str):  # Handle missing skills
            skills = []
        else:
            skills = [skill.strip() for skill in str(skills_str).split(',')]
        
        # Keep only latest entry per user
        latest_skills[name] = skills

    extracted_data = []
    for name, skills in latest_skills.items():
        extracted_data.append((name, skills[:top_n]))  # Take top N skills

    return extracted_data


if __name__ == "__main__":
    csv_path = "extracted_resume_data.csv"
    data = extract_skills_from_csv(csv_path)
    print(data)
