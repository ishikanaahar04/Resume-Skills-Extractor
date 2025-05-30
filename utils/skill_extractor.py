import pandas as pd

def extract_skills_from_csv(csv_path):
    df = pd.read_csv(csv_path)
    extracted_data = []
    for index, row in df.iterrows():
        name = row['Name']
        skills = [skill.strip() for skill in row['Skills'].split(',')]
        top_five = skills[:5]
        extracted_data.append((name, top_five))
    return extracted_data

# This will only run if you execute this file directly
if __name__ == "__main__":
    csv_path = "extracted_resume_data.csv"  # <-- Update with the real path
    data = extract_skills_from_csv(csv_path)
    print(data)
