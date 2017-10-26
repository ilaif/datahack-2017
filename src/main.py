from main_util import load_questions, extract_features

if __name__ == '__main__':
    print('Loading questions..')
    questions = load_questions()
    print('Extracting features..')
    extract_features(questions)

    for q in questions[:50]:
        print([a.common_synonyms_with_question_count for a in q.answers])
