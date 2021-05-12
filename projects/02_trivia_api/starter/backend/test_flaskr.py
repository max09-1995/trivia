import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category, db


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    

        # Create Test Object
     
        self.new_Question = {
            'question':'What is the tallest building',
            'answer':'burjdubai',
            'category':'4',
            'difficulty':'2'
        }
       
    def tearDown(self):
        """Executed after reach test"""
        pass

    
    """
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_getsimilarquestions(self):
        res = self.client().get('/questions/search')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code,200)
        self.assertGreaterEqual(data[0]['totalQuestions'], 0)

    def test_getallquestions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code,200)
        self.assertGreaterEqual(data[0]['totalquestions'], 0)


    def test_post_new_question(self):
        res = self.client().post('/question/create', data=self.new_Question)
        
        self.assertEqual(res.status_code,200)

        question = db.session.query(Question).filter_by(answer='burjdubai')
        #filter query should not return null
        global filter_id 
        filter_id = question[0].id
        self.assertIsNotNone(question)

    def test_getspecificquestion(self):
        
        question = db.session.query(Question).filter_by(answer='burjdubai')
        filter_id = question[0].id

        #url = f'/question/{filter_id}'
        url = '/question/' + filter_id
        print(url)
    
        #res = self.client().post(f'{url}')
        res = self.client().post(url)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data[0]['question'],'What is the tallest building')
        self.assertEqual(data[0]['answer'], 'burjdubai')
    
    def test_deletequestion(self):
        
            #  Create entry --> Executed in previous test
        
        question = db.session.query(Question).filter_by(answer='burjdubai')
        filter_id = question[0].id
        
        
        res = self.client().delete('/question/delete', data={'id':filter_id})
        
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        
    def test_getquestionscategory(self):

        res = self.client().post('/play/quiz')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(data[0]['question'])
        self.assertIsNotNone(data[0]['answer'])

    def test_playquestion(self):

        res = self.client().post('/play/quiz')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertIsNotNone(data[0]['question'])
        self.assertIsNotNone(data[0]['answer'])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
    