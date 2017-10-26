from main_util import load_questions, extract_features, build_df

if __name__ == '__main__':
    print('Loading questions..')
    questions = load_questions()
    print('Extracting features..')
    extract_features(questions)
    print('Build df')
    pd = build_df(questions)

    print(pd)
