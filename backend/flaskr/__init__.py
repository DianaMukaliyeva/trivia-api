import os
import random
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginated_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    paginated_questions = questions[start:end]
    return paginated_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={r'/*': {'origins': '*'}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                            'Content-Type, Authorization, True')
        response.headers.add('Access-Control-Allow-Methods',
                            'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/categories')
    def list_categories():
        response = {}
        categories = Category.query.all()
        for category in categories:
            response[category.id] = category.type
        return jsonify({
            'categories': response
        })

    @app.route('/questions')
    def list_questions():
        selection = Question.query.order_by(Question.id).all()
        questions = paginated_questions(request, selection)
        if len(questions) == 0 and len(selection) != 0:
            return abort(404)
        categories = {}
        for category in Category.query.all():
            categories[category.id] = category.type
        return jsonify({
            'questions': questions,
            'total_questions': len(selection),
            'categories': categories,
            'current_category': None
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            question.delete()
            return jsonify({
                'deleted': question_id
            })
        except:
            abort(422)

    @app.route('/search', methods=['POST'])
    def search_question():
        body = request.get_json()
        try:
            search_term = body.get('searchTerm')
            selection = Question.query\
                .order_by(Question.id)\
                .filter(Question.question.ilike(f'%{search_term}%'))\
                .all()
            questions = paginated_questions(request, selection)
            if len(questions) == 0 and len(selection) != 0:
                return abort(404)
            return jsonify({
                'questions': questions,
                'total_questions': len(questions),
                'current_category': None
            })
        except:
            abort(400)

    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        try:
            question_text = body.get('question')
            answer_text = body.get('answer')
            difficulty = body.get('difficulty')
            category = body.get('category')
            new_question = Question(
                question_text,
                answer_text,
                category,
                difficulty
            )
            new_question.insert()
            return jsonify({
                'success': True,
                'created': new_question.id
            })
        except:
            abort(400)

    @app.route('/categories/<int:category_id>/questions')
    def list_categories_questions(category_id):
        try:
            category = Category.query.get(category_id)
            selection = Question.query.order_by(Question.id)\
                        .filter(Question.category == category_id).all()
            questions = paginated_questions(request, selection)
            if len(questions) == 0 and len(selection) != 0:
                return abort(404)
            return jsonify({
                'questions': questions,
                'total_questions': len(selection),
                'current_category': {category.id: category.type}
            })
        except:
            abort(404)

    @app.route('/quizzes', methods=['POST'])
    def get_next_questions():
        body = request.get_json()
        try:
            previous_questions = body.get('previous_questions')
            quiz_category = body.get('quiz_category')
            if quiz_category['id'] == 0:
                category_questions = Question.query.all()
            else:
                category_questions = Question.query\
                    .filter(Question.category == quiz_category['id'])\
                    .all()
            left_questions = []
            for question in category_questions:
                if question.id  not in previous_questions:
                    left_questions.append(question.format())
            if left_questions:
                next_question = random.choice(left_questions)
            else:
                next_question = None
            return jsonify({
                'question': next_question
            })
        except:
            abort(400)

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify ({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify ({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify ({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify ({
            'success': False,
            'error': 500,
            'message': 'something went wrong'
        }), 500

    return app
