def run_quiz(questions_text):
    questions = questions_text.strip().split("\n\n")  # Each question block separated by empty line
    score = 0

    for q in questions:
        lines = q.split('\n')
        
        # Filter out the answer line so it won't be shown before user answers
        question_lines = [line for line in lines if not line.startswith("Answer:")]
        
        # Print question and options
        for line in question_lines:
            print(line)
        
        # Get user answer
        answer = input("Your answer (A/B/C/D): ").strip().upper()

        # Extract correct answer from answer line
        correct_line = [line for line in lines if line.startswith("Answer:")]
        if correct_line:
            correct_answer = correct_line[0].split(":")[1].strip().upper()
            if answer == correct_answer:
                score += 1
                print("✅ Correct!\n")
            else:
                print(f"❌ Wrong! Correct answer was: {correct_answer}\n")
        else:
            print("⚠️ Could not find correct answer line.\n")

    return score
