# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## API Documentation


GET '/categories'
- Fetches a dictionary of categories.
- Request Arguments: None
- Returns: An object including a dictionary including all availble categories.
{
    "categories": [
        0,
        1,
        2,
        3,
        4
    ]
}


GET '/questions'

- Fetches a dictionary of categories, the number of totalquestions and a dictionary of questions. Each question contains the attribute answer, category, difficulty, id and the question itself.
- Request Arguments: None
- Returns: A dictionary of categories, questions and a integer value for the number of questions in the dictionary questions.
{
    "categories": [
        1,
        2,
        3,
        4,
        5
    ],
    "questions": [
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
    ],
    "totalquestions": 4
}

POST '/questions/search'

- Fetches a dictionary of questions that are matching the search criteria. Further the amount of total questions is returned.
- Request Arguments: A searchTerm needs to be sent:
    {"searchTerm":"Cassius Clay"}
- Returns: An object with the currentCategory, all questions in an dictionary that are matching to the searchTerm in a dictionary and the totalQuestions.
{
    "currentCategory": 4,
    "questions": [
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        }
    ],
    "totalQuestions": 1
}

DELETE '/question/delete'

- Deletes the row of the question with the specified id in the database
- Request Arguments: The ID of the question needs to be specified
    {"id":"10"}
- Returns: Returns the status code and success of the request.
    {
    "status_code": 200,
    "successfull": true
    }

POST '/question/create'

- Creates a new question in the database for the specified parameters
- Request Arguments: The question, answer, category and difficulty needs to be sent as JSON:
    {
    "question":"Add the question here",
    "answer":"Add the answer over here",
    "category": "4",
    "difficulty":"2"
}
- Returns: Returns the status code and success of the request.
{
    "status_code": 200,
    "successfull": true
}

POST '/question/<id>'

- Fetches a dictionary of a question for the specified id
- Request Arguments: The id needs to be defined in the URL
- Returns: An object with the answer, question, category and difficulty is returned
[
    {
        "answer": "George Washington Carver",
        "category": 4,
        "difficulty": 2,
        "question": "Who invented Peanut Butter?"
    }
]

POST '/question/category/<category>'

- Fetches a dictionary of all questions for the specified category
- Request Arguments: The category needs to be defined in the URL
- Returns: An object with the currentCategory, all questions in a dictionary of the specified category and the totalQuestions.

{
    "currenCategory": "2",
    "questions": [
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "question": "In which royal palace would you find the Hall of Mirrors?"
        },
        {
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "question": "The Taj Mahal is located in which Indian city?"
        }
    ],
    "totalQuestions": 3
}

POST '/play/quiz'

- Fetches the next question for the quiz
- Request Arguments: The previous questions need to defined in a dictionary object. Further the category needs to be defined. If "All" is selected the type is called "click", all others are named according to the categories defined in the get category call.
{
    "previous_questions":[1,2,3],
    "quiz_category":{
        "type":"click"
    }

}
- Returns: An dictionary object including question, answer, category, difficulty and id 

{
    "question": {
        "answer": "Muhammad Ali",
        "category": 4,
        "difficulty": 1,
        "id": 9,
        "question": "What boxer's original name is Cassius Clay?"
    }
}