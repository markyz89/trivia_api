import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
  
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions
    

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODUN: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODUNs
  '''
  cors = CORS(app, resources={r"*": {"origins" : "*"}})

  '''
  @TODUN: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response

  '''
  @TODUN: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''

  @app.route('/categories')
  def get_categories():
    categories = Category.query.all()

    categories_formatted = {}
    
    for category in categories:
      categories_formatted[category.id] = category.type

    return jsonify({
      'success': True,
      'categories': categories_formatted
    })


  



  '''
  @TODUN: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  
  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def get_questions():
    selection = Question.query.order_by(Question.id).all()

    current_questions = paginate_questions(request, selection)

    categories = Category.query.all()

    categories_formatted = {}
    
    for category in categories:
      categories_formatted[category.id] = category.type

    if len(current_questions) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(Question.query.all()),
      'categories': categories_formatted
    })
    



  '''
  @TODUN: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      if question is None:
        abort(404)

      question.delete()
      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)
      
      return jsonify({
        'success' : True,
        'deleted' : question_id,
        'questions': current_questions,
        'total_questions': len(Question.query.all())
      })
    except:
      abort(422)
    



  '''
  @TODUN: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():
    body = request.get_json()


    try:
      q = Question(question=body.get('question', None), answer=body.get('answer', None), category=body.get('category', None), difficulty=body.get('difficulty', None))
      q.insert()

      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)

      return jsonify({
        'success': True,
        'created': q.id,
        'questions': current_questions,
        'total_questions': len(Question.query.all())
      })

    except:
      
      abort(422)

  
  '''
  @TODUN: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  @app.route('/questions/search', methods=['POST'])
  def search_question():

    body = request.get_json()
    search = body.get('searchTerm', None)

    selection = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search)))
    current_questions = paginate_questions(request, selection)

    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(selection.all())
    })

  '''
  @TODUN: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

  @app.route('/categories/<int:category_id>/questions/')
  def get_questions_by_category(category_id):
    selection = Question.query.filter(Question.category == category_id).all()

    questions = [question.format() for question in selection]

    categories = Category.query.all()

    categories_formatted = {}
    
    for category in categories:
      categories_formatted[category.id] = category.type


    if len(questions) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': questions,
      'total_questions': len(selection),
      'categories': categories_formatted
    })

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  @app.route('/quizzes', methods=['POST'])
  def generate_quiz_questions():
    body = request.get_json()

    previous_questions = body.get('previous_questions', None)
    quiz_category = body.get('quiz_category')

    print(quiz_category)

    #getting the questions by category, or all
    if(quiz_category['id']):
      selection = Question.query.filter(Question.category == quiz_category['id']).all()
    else:
      selection = Question.query.all()

    #formatting
    questions = {}
    for question in selection:
      questions[question.id] = question

    #filtering to exclude already asked questions
    filtered_selection = {key: question for key, question in questions.items() if key not in previous_questions}
    if (filtered_selection):
      question = random.choice(list(filtered_selection.values())).format()
    else:
      question = 0

    print(previous_questions)
    # print(questions)
    # print(filtered_selection)
    # print(question)

    return jsonify({
      'success': True,
      'question': question
    })



  '''
  @TODUN: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "resource not found"
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "unprocessable"
      }), 422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "bad request"
      }), 400

  @app.errorhandler(405)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 405,
      "message": "method not allowed"
      }), 405
  
  return app

    