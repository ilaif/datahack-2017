from src.main_util import load_questions_string, extract_features, build_df

if __name__ == '__main__':
    s = """A marginal change is a
0 long-term trend.
0 change for the worse.
1 small incremental adjustment.
0 large, significant adjustment."""
    questions = load_questions_string(s, 'shit')
    extract_features(questions)
    pd = build_df(questions)
    print(pd)
