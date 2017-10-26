import sklearn
from sklearn.ensemble import IsolationForest
# from sklearn.model_selection import train_test_split
import numpy as np


def generate_forest(train, tests):
    """
    train an isolation tree on trains set and predict on each test (suppose to be 4 tests)
    :param train:
    :param tests:
    :return:
    """
    clf = IsolationForest(max_sample=1000, random_state=0, contamination=0, verbose=1)
    clf.fit(train)
    # y_pred_train = clf.predict(train)
    y_pred_tests = [clf.predict(test) for test in tests]

    return np.transpose(y_pred_tests)


def parse_results(res, test):
    """
    :param res: An n x 4 array - each row presents the scores of each possible choice
    :param test: test in Question object format
    :return: array of size n of all correct answers
    """
    print "error is: " + str(np.count_nonzero([max(x) - test[x].correct_answer_idx for x in res]) / float(len(res)))
    return [max(x) - test[x].correct_answer_idx for x in res]


if __name__ == "__main__":
    pass
    # train, test = train_test_split(df, test_size=0.25, train_size=0.75)
    # generate_forest(df)