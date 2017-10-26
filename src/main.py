from main_util import load_questions, extract_features, build_df

if __name__ == '__main__':
    print('Loading questions..')
    questions = load_questions()
    print('Extracting features..')
    extract_features(questions)
    print('Building df..')
    pd = build_df(questions)
    print('Done')

    print(pd)
