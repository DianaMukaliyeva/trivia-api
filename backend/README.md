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
createdb trivia
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

## API Documentation

#### GET '/categories'

  * Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
  * Request Arguments: None
  * Response: An object with a single key, categories, that contains an object of id: category_string key:value pairs. 
  * Sample:  `curl localhost:5000/categories`
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```

#### GET '/questions?page=1'

  * Fetches the questions to be displayed on the page.
  * Request Arguments: `page`. By default value of page = 1.
  * Response: a list of question objects, a dictionary of categories, current category and total number of questions as JSON object. Results of questions are paginated in groups of 10.
  * Sample:  `curl localhost:5000/questions?page=2`
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
  ],
  "total_questions": 1
}
```

#### DELETE '/questions/{question_id}'

  * Deletes the question of the given ID if it exists.
  * Request Parameters: `question_id`. ID of the existing question
  * Response: the ID of the deleted question.
  * Sample:  `curl localhost:5000/questions/22 -X DELETE`
```
{
  "deleted": 22
}
```

#### POST '/search'

    * Search for all questions that have a given search string in the question field.
    * Returns a list of question objects, current category and total number of returned questions as JSON object.
    * Request Arguments: `searchTerm`. The search phrase.
    * Results of questions are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
    * Sample:
         `curl localhost:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "movie"}'`
```
{
  "current_category": null,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
  ],
  "total_questions": 1
}
```

#### POST '/questions'

    * Creates new question
    * Creates a new question using the submitted question, answer, category and difficulty. Return the ID of the created book and success value.
    * Request Arguments:
    `question` - statement of a question,
    `answer` - statement of an answer,
    `category` - ID of category,
    `difficulty` - difficulty level from 1 to 5.
    * Sample:
         ```
         curl localhost:5000/questions -X POST -H "Content-Type: application/json" -d '{
             "question": "Hiiii",
             "answer": "kokokokok",
             "difficulty": "3",
             "category": "1"
         }'
         ```
```
{
  "created": 24,
  "success": true
}
```

#### GET '/categories/{category_id}/questions'

  * Fetches the questions for the requested category to be displayed on the page.
  * Request Parameters: `category_id`. The ID of the existing category.
  * Response: a list of question objects, current category and total number of questions in this category as JSON object.
  * Sample: `curl localhost:5000/categories/2/questions`
```
{
  "current_category": {
    "2": "Art"
  },
  "questions": [
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ],
  "total_questions": 4
}
```

#### POST '/quizzes'

  * Fetches a random question within the given category, that is not one of the previous questions.
  * Request Arguments: 
  `previous_questions` - list of already answered questions,
  `quiz_category` - the given category object.
  * Response: the random question object as JSON object.
  * Sample:  
       ```
          curl localhost:5000/quizzes -X POST -H "Content-Type: application/json" -d '{
               "previous_questions": [],
               "quiz_category": {"type":"History", "id":1}
          }'
       ```
```
{
  "question": {
    "answer": "Alexander Fleming",
    "category": 1,
    "difficulty": 3,
    "id": 21,
    "question": "Who discovered penicillin?"
  }
}
```

## Error Handling

This application uses convential HTTP response codes to indicate a success or a failure.
Errors are returned as JSON objects in the following format:

```
{
    'success': True
    'error': 400,
    'message': 'bad request'
}
```

The API return three error types when request fails:

* 400: Bad Request
* 404: Resource Not Found
* 422: Not Processable


## Testing
To run the tests, run
```
dropdb --if-exists trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
