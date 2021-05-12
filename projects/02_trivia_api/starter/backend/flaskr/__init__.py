import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy, Pagination
from flask_cors import CORS
import random
from  sqlalchemy.sql.expression import func, select

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  
 # @: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  cors = CORS(app)
  
  #@: Testing, nicht hundertprozentig klar was das Dictionary macht
  cors = CORS(app, resources={r"/api/*": {"origins": "/question"}})
  
  #@: Use the after_request decorator to set Access-Control-Allow

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Origion', '*')
    
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response
  

  #@: Create an endpoint to handle GET requests 
  #for all available categories.
  


  '''
  @: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  @app.route('/questions/search', methods=['POST']) 
  def getsimilarquestions():
    try:
      #get data
      data = request.get_json()
      search = data['searchTerm']
      search = '%' + search + '%'
      
      #access database
      query_result = Question.query.filter(Question.question.like(search)).all()
    

      counter = 0
      currenCategory = 0
      all_questions = []

      for q in query_result:
        counter = counter + 1
        currenCategory = q.category

        question12 = {}
        question12['id'] = q.id
        question12['answer'] = q.answer
        question12['question'] = q.question
        question12['difficulty'] = q.difficulty
        question12['category'] = q.category

        all_questions.append(question12)
    
        result = {
          'questions': all_questions,
          'totalQuestions': counter,
          'currentCategory':currenCategory
        }
    except:

      abort(500)

    return jsonify(result)

  @app.route('/questions', methods=['GET'])
  def get_questions():
    page = request.args.get('page', default = 1, type = int)
    
    result = Question.query.paginate(page,per_page=10)
    
    db_query = db.session.query(Question).all()
    
    pagecounter = 0
    totalquestion = 0
    pageno = 0
    all_questions = []
    page_content = [] 


    for q in db_query:

      totalquestion = totalquestion + 1
      pagecounter = pagecounter +1

      question12 = {}
      question12['id'] = q.id
      question12['answer'] = q.answer
      question12['question'] = q.question
      question12['difficulty'] = q.difficulty
      question12['category'] = q.category


      all_questions.append(question12)

      if pagecounter == 10:
       
        pagecounter = 0
        pageno = pageno + 1
        
    page_content = all_questions
    
    
   
    result = {"totalquestions":totalquestion, "questions": page_content, "categories":[1,2,3,4,5]}
    
    return jsonify(result)
    

  '''
  @: Testing
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  
              

  @app.route('/question/delete', methods=['DELETE'])
  def deletequestion():
   
    try:
      data = request.get_json()
      #print(data)
      
      question_object = Question.query.get(data['id'])

      db.session.delete(question_object)

      db.session.commit()
      
    except:
      print("an error occured")
      db.session.rollback()
      abort(400)

    finally:
      db.session.close()

    return jsonify({"status_code":200,"successfull":True})
  '''
  @: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/question/create', methods=['POST'])
  def postanewquestion():
    try:
      
      form = request.get_json()
      print(form)
      
      question = Question(question=form['question'],answer=form['answer'], category=form['category'], difficulty=form['difficulty'])
      Question.insert(question)
     

    except:
      print("not successfull")
      db.session.rollback()
      abort(400)
  

    finally:
      
      db.session.close()
      
    return jsonify({"status_code":200,"successfull":True})
    

  '''
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/question/<id>', methods=['POST'])
  def getspecificquestion(id):

    try:
      question = db.session.query(Question).filter_by(id=id)

      data = [
        {
        "question":question[0].question,
        "answer":question[0].answer,
        "category":question[0].category,
        "difficulty":question[0].difficulty
      }
      ]
    except:
      abort(400)

    return jsonify(data)
  '''
  
  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/question/category/<category>', methods=['POST'])
  def getquestionsforcategory(category):
    try:
      
      number = int(category) +1
     

      questions = db.session.query(Question).filter_by(category=number)

      data2 = []
      data1 = {}
      total = 0
      
      for question in questions:
        total = total + 1
        data = {
        "question":question.question,
        "answer":question.answer,
        "category":question.category,
        "difficulty":question.difficulty
        }
        
        data2.append(data)
      data1 = {
        "questions":data2,
        "totalQuestions":total,
        "currenCategory": category
      }
    except:
      print("not working")
      abort(500)

    finally:
      db.session.close()

    return jsonify(data1)


  '''
  @: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/play/quiz', methods=['POST'])
  def playquestion():
    try:
      
      data1 = {}

      # Get Data from request body
      data = request.get_json()
      previous_questions = data['previous_questions']
      category = data['quiz_category']['type']
      
      if category == 'click':
        
        questions = db.session.query(Question).filter(~Question.id.in_(previous_questions)).order_by(func.random())
        
        
      else:
     
        questions = db.session.query(Question).filter(~Question.id.in_(previous_questions)).filter_by(category=category).order_by(func.random())
        
      for question in questions:
        data1 = {}
        data1 = {
        'question':question.question,
        'answer':question.answer,
        'category':question.category,
        'difficulty':question.difficulty,
        'id':question.id
        }
      result = {'question': data1}
      
    except:
      abort(400)
      print("exception raised")
    finally:

      db.session.close()

   
    return jsonify(result)
  
  @app.route('/categories', methods=['GET'])
  def getcategories():

    data = {
      'categories':[0,1,2,3,4]
    }

    return jsonify(data)
  '''
  @: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(500)
  def servererror(error):
    return 'internal server error: 500 ', 500
  
  @app.errorhandler(400)
  def badrequest():
    return 'bad request, 400', 400
  

  @app.errorhandler(422)
  def unprocessable_entity():
    return 'unprocessable entity: 422', 422

  @app.errorhandler(404)
  def unprocessable_entity():
    return 'page not found: 404', 404
  
  return app