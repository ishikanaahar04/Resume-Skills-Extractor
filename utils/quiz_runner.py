def run_quiz(questions_list):
    score = 0
    total = len(questions_list)

    for idx, q in enumerate(questions_list, 1):
        print(f"\nQ{idx}: {q['question']}")

        # Print options directly (already have A/B/C/D from generator)
        for opt in q['options']:
            print(opt)

        answer = input("Your answer (A-D): ").strip().upper()

        if answer == q['answer']:
            print("✅ Correct!")
            score += 1
        else:
            print(f"❌ Wrong! Correct answer: {q['answer']}")

    print(f"\nFinal Score: {score} / {total}")
    return score   # ✅ return score so main.py can use it
