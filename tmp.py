from src import main

questions = main.load_questions(folder_path='./MCQ/')

chars = set()
for q in questions:
    chars.update({c for c in q.text})
    for a in q.answers:
        chars.update({c for c in a.text})

print(chars)
