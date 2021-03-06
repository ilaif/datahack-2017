def build_attributes_dict(obj, features_list, prefix):
    features = {}
    for feature_name in features_list:
        features[prefix + feature_name] = getattr(obj, feature_name)
    return features


class Question(object):
    def __init__(self, question, category):
        self.text = question
        self.category = category
        self.answers = []
        self.correct_answer_idx = None
        self.original_correct_answer_idx = None
        self.answersGraph = {}

        # Features
        self.num_answers = None
        self.char_count = None
        self.word_count = None
        self.stopword_count = None
        self.without_stopword_count = None
        self.is_completion = None  # Whether has __ in the sentence
        self.is_question = None  # Whether "ends" with '?'
        self.average_frequency = None
        self.title_count = None

    def add_answer(self, answer):
        self.answers.append(answer)
        cur_idx = len(self.answers) - 1
        if answer.is_correct:
            self.correct_answer_idx = cur_idx
            self.original_correct_answer_idx = cur_idx
        for i in range(len(self.answers) - 1):
            ar = AnswerRelation(from_idx=i, to_idx=cur_idx)
            self.answersGraph[(i, cur_idx)] = ar
        self.num_answers = len(self.answers)

    def swap_answers(self, i, j):
        if i == j:
            return

        tmp = self.answers[i]
        self.answers[i] = self.answers[j]
        self.answers[j] = tmp

        # Swap translation dict
        trans_d = {x: x for x in range(self.num_answers)}
        trans_d[i] = j
        trans_d[j] = i

        d = {}
        ag = self.answersGraph

        for k in range(self.num_answers):
            for m in range(k + 1, self.num_answers):
                new_key = tuple(sorted([trans_d[k], trans_d[m]]))
                d[new_key] = ag[(k, m)]
                ag[(k, m)].from_idx = new_key[0]
                ag[(k, m)].to_idx = new_key[1]

        self.answersGraph = d
        self.correct_answer_idx = trans_d[self.correct_answer_idx]

    def get_raw_attributes(self):
        return {'q_text': self.text, 'q_category': self.category, 'q_correct_answer_idx': self.correct_answer_idx}

    @staticmethod
    def get_features_list():
        return ['num_answers', 'char_count', 'word_count', 'stopword_count', 'without_stopword_count',
                'is_completion', 'is_question', 'average_frequency', 'title_count']

    def get_features(self):
        return build_attributes_dict(self, self.get_features_list(), 'q_')

        # def __repr__(self):
        #     answers_repr = ''
        #     for i, a in enumerate(self.answers):
        #         answer = a.text
        #         if self.correct_answer_idx == i:
        #             answers_repr += '*('
        #         if len(answer) > 10:
        #             answer = answer[:10] + '..'
        #         else:
        #             answer = answer[:10]
        #         answers_repr += answer
        #         if self.correct_answer_idx == i:
        #             answers_repr += ')*)'
        #         if i < len(self.answers) - 1:
        #             answers_repr += ', '
        #     return 'Q(%s), A[%s]' % (self.text[:15] + '..', answers_repr)


class Answer(object):
    def __init__(self, answer, is_correct):
        self.is_correct = is_correct
        self.text = answer

        # Features
        self.char_count = None
        self.word_count = None
        self.stopword_count = None
        self.without_stopword_count = None
        self.common_words_with_question_count = None
        self.common_synonyms_with_question_count = None
        self.certainty_count = None
        self.all_or_none = None
        self.average_frequency = None
        self.similarity_with_question = None
        self.title_count = None

    def get_raw_attributes(self, idx=''):
        if idx is not '':
            idx = '%s_' % idx
        return {'a_%stext' % idx: self.text, 'a_%sis_correct' % idx: self.is_correct}

    def get_features(self, idx=''):
        if idx is not '':
            idx = '%s_' % idx
        features_list = ['char_count', 'word_count', 'stopword_count', 'without_stopword_count',
                         'common_words_with_question_count', 'common_synonyms_with_question_count', 'certainty_count',
                         'all_or_none', 'average_frequency', 'similarity_with_question', 'title_count']
        return build_attributes_dict(self, features_list, 'a_%s' % idx)


class AnswerRelation(object):
    def __init__(self, from_idx, to_idx):
        self.from_idx = from_idx
        self.to_idx = to_idx

        self.similarity = None
        self.synonyms_count = None

    def get_raw_attributes(self):
        return {}  # TODO:

    def get_features(self):
        features_list = ['similarity', 'synonyms_count']
        return build_attributes_dict(self, features_list, 'ar_%s_%s_' % (self.from_idx, self.to_idx))
