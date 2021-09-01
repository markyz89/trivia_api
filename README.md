# Full Stack API Final Project


## Full Stack Trivia

The Full Stack Trivia API is an application designed to test your general knowledge and the developer's skill's as a full-stack API. The front-end was created by Udacity and the task was to create a backend which via an API could: 

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.


## Installation

### Frontend

You will require Node and NPM to run the frontend. Once you have these installed, all other dependencies can be installed by opening the frontend directory in your terminal and running:

```
npm install
```
Run the frontend server with:
```
npm start
```

>View the [README within ./frontend for more details.](./frontend/README.md)

### Backend

For the backend you will require Python3 and pip. Python 3.7 is recommended.

Once these are installed, to install all other backend dependencies, you should run:

```
pip install -r requirements.txt
```

A starter postgres database file has also been provided. To turn this into a functioning database, from within your backend folder run:

```
psql trivia < trivia.psql
```
Run the server with:

```
flask run
```

## API Reference

### Getting Started

Base URL: This app can presently only be run locally. The backend app is hosted at the default http://127.0.0.1:5000/

Authentication: This version of the project does not include authentication or API Keys.

### Errors

Errors are returned as JSON objects in the following format:

```
{
  "success": False,
  "error": 400,
  "message": "bad request"
}

```

The API will return four error types when requests fail:

* 400 Bad Request
* 404 Resource Not Found
* 405 Not Allowed
* 422 Unprocessable

### Resource Endpoint Library

### GET /categories

* General
   - Returns the list of categories as an object and a success value.
* Sample: ```curl http://127.0.0.1:5000/categories ```

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
    "success": true
}
```

### GET /questions
* General
   - Returns the list of questions as an object, a success value and the total number of questions.
   - Results are paginated into groups of 10
* Sample: ```curl http://127.0.0.1:5000/questions?page=3 ```

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
    "questions": [
        {
            "answer": "One",
            "category": 6,
            "difficulty": 1,
            "id": 25,
            "question": "How many clubs did Francesco Totti play for?"
        }
    ],
    "success": true,
    "total_questions": 21
}

```

### DELETE questions/<id>
* General
   - Deletes a question from the database
   - Returns a list of the remaining questions, a success value and the total questions
* Sample: ```curl http://127.0.0.1:5000/delete/25 -X DELETE```

```
{
    "deleted": 25,
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        ...
        {
            "answer": "A fruit",
            "category": 2,
            "difficulty": 1,
            "id": 24,
            "question": "What is a banana?"
        }
    ],
    "success": true,
    "total_questions": 20
}
```

### POST /question
* General
   - Creates a new question and adds it to the database
   - Returns a list of questions including the newly added one, a success value and the total questions
* Sample: ```curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"answer": "A vegetable", "category": 1, "difficulty": 1, "id": 28, "question": "What is a cabbage?"}'```
```
{
    "created": 28,
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        ...
        {
            "answer": "A vegetable",
            "category": 1,
            "difficulty": 1,
            "id": 28,
            "question": "What is a cabbage?"
        }
    ],
    "success": true,
    "total_questions": 21
}
```

### POST questions/search
* General
   - Searches for the question within the database using the search term
   - Returns a list of questions where the search term is included somewhere within the question, a success value and the total questions
* Sample: ```curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm": "Hanks"}'```

```
{
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        }
    ],
    "success": true,
    "total_questions": 1
}
```

### GET /categories/<id>/questions 

* General
   - Gets questions based on the category id
   - Returns a list of questions which match the category id, a success value and the total questions
* Sample: ```curl http://127.0.0.1:5000/categories/1/questions'```

```
{
    "questions": [
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        },
        {
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
        },
        {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
        }
    ],
    "success": true,
    "total_questions": 3
}
```

### POST /quizzes
* General
   - Returns a random question based on category and previous question parameters in order to play the quiz.
   - Returns one question which matches the category id and is not included in the list of previous questions and a success value.

```curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions" : [], "quiz_category": {"type": "Science", "id": "1"}}'```
```
{
    "question": {
        "answer": "Alexander Fleming",
        "category": 1,
        "difficulty": 3,
        "id": 21,
        "question": "Who discovered penicillin?"
    },
    "success": true
}
```

## Authors
Mark Simpson contributed to the __init__.py and test_flaskr.py files in the backend. All other files were created by Udacity.