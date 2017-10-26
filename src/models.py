class Question(object):
    def __init__(self, question, category):
        self.text = question
        self.category = category
        self.answers = []
        self.correct_answer_idx = None
        self.answersGraph = {}

        # Features
        self.char_count = None
        self.word_count = None
        self.stopword_count = None
        self.without_stopword_count = None

    def add_answer(self, answer, is_correct):
        self.answers.append(Answer(answer, is_correct))
        cur_idx = len(self.answers) - 1
        if is_correct:
            self.correct_answer_idx = cur_idx

        for i in range(len(self.answers)):
            self.answersGraph[(i, cur_idx)] = AnswerRelation()
            self.answersGraph[(cur_idx, i)] = AnswerRelation()

    def get_features(self):
        return {
            'question_char_count': self.char_count,
            'question_word_count': self.word_count
        }

    def __repr__(self):
        answers_repr = ''
        for i, a in enumerate(self.answers):
            answer = a.text
            if self.correct_answer_idx == i:
                answers_repr += '*('
            if len(answer) > 10:
                answer = answer[:10] + '..'
            else:
                answer = answer[:10]
            answers_repr += answer
            if self.correct_answer_idx == i:
                answers_repr += ')*)'
            if i < len(self.answers) - 1:
                answers_repr += ', '
        return 'Q(%s), A[%s]' % (self.text[:15] + '..', answers_repr)


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


class AnswerRelation(object):
    def __init__(self):
        pass
