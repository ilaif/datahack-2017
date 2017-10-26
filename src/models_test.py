import unittest

from models import Question


class TesQuestionModel(unittest.TestCase):
    def test_check_swaps(self):
        q = Question('Question', 'Category')
        q.add_answer('Answer 1', False)
        q.add_answer('Answer 2', False)
        q.add_answer('Answer 3', True)
        q.add_answer('Answer 4', False)
        ag = q.answersGraph
        ag[(0, 1)].similarity = '0,1'
        ag[(0, 2)].similarity = '0,2'
        ag[(0, 3)].similarity = '0,3'
        ag[(1, 2)].similarity = '1,2'
        ag[(1, 3)].similarity = '1,3'
        ag[(2, 3)].similarity = '2,3'

        q.swap_answers(0, 2)
        ag = q.answersGraph

        self.assertEqual(ag[(0, 1)].similarity, '1,2')
        self.assertEqual(ag[(0, 2)].similarity, '0,2')
        self.assertEqual(ag[(0, 3)].similarity, '2,3')
        self.assertEqual(ag[(1, 2)].similarity, '0,1')
        self.assertEqual(ag[(1, 3)].similarity, '1,3')
        self.assertEqual(ag[(2, 3)].similarity, '0,3')
