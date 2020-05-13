import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}"\
            .format('postgres', 'postgres', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'How are you?',
            'answer': 'Good',
            'category': '1',
            'difficulty': '1'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])

    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        questions = Question.query.all()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['total_questions'], len(questions))
        self.assertTrue(data['questions'])

    def test_get_questions_fail_if_page_beyond_valid(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_question(self):
        res = self.client().delete('/questions/22')
        data = json.loads(res.data)
        question = Question.query.get(22)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(question, None)
        self.assertEqual(data['deleted'], 22)

    def test_delete_question_if_not_exists(self):
        res = self.client().delete('/questions/220')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_create_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['created'])

    def test_question_creation_not_allowed(self):
        res = self.client().post('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_successful_search(self):
        res = self.client().post('/search', json={'searchTerm': 'how'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    def test_search_with_no_result(self):
        res = self.client().post('/search', json={'searchTerm': 'jdiojoijoijoj'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['questions']), 0)
        self.assertEqual(data['total_questions'], 0)

    def test_get_questions_for_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    def test_get_questions_for_not_existing_category(self):
        res = self.client().get('/categories/9/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_question_for_quiz_by_category(self):
        res = self.client().post('/quizzes',
            json={
                'previous_questions': [],
                'quiz_category': {'type': 'Science', 'id': 1}
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])

    def test_get_all_questions_for_quiz(self):
        res = self.client().post('/quizzes',
            json={
                'previous_questions': [],
                'quiz_category': {'type': 'click', 'id': 0}
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])

    def test_no_questions_for_quiz_left(self):
        res = self.client().post('/quizzes',
            json={
                'previous_questions': [20, 21, 22, 24],
                'quiz_category': {'type': 'Science', 'id': 1}
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertFalse(data['question'])

    def test_failed_to_get_question_for_quiz(self):
        res = self.client().post('/quizzes')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()