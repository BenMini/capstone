from flask import redirect, url_for, request, jsonify, current_app
from app import db
from app.models import Business, Post
from app.main import bp
from .auth.auth import AuthError, requires_auth

POSTS_PER_PAGE = 10


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


def paginate_posts(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * POSTS_PER_PAGE
    end = start + POSTS_PER_PAGE

    posts = [post.short() for post in selection]
    current_posts = posts[start:end]
    return current_posts


'''
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
'''
db_drop_and_create_all()

# ---------------------------------------------------------------
# Business Routes
# ---------------------------------------------------------------
@bp.route('/', methods=['GET', 'POST'])
def businesses():
    if request.method == 'GET':
        def directory():
            '''lists all businesses in short form'''
            try:
                return jsonify({
                    'success': True,
                    'businesses': [
                        business.short() for business in Business.query.all()]
                }), 200
            except Exception as e:
                print(e)
                abort(404)
        return directory()

    if requst.method == 'POST':
        @requires_auth('post:business')
        def create_business(payload):
            '''Creates a new business'''
            try:
                new_business = Business(
                    name=request.json['name'],
                    email=request.json['email'],
                    phone=request.json['phone'],
                    description=request.json['description'])
                new_business.insert()
                return jsonify({
                    'success': True,
                    'business': [new_business.long()]
                }), 200
            except Exception as e:
                print(e)
                abort(422)


@bp.route('/business/<bus_id>', methods=['GET', 'PATCH', 'DELETE'])
def businesse_functions():
    if request.method == 'GET':
        def get_business_detail(bus_id):
            try:
                business = Business.query.filter(
                    Business.id == bus_id).first()
                selection = business.posts.order_by(
                    Post.timestamp.desc()).all()
                current_posts = paginate_posts(request, selection)

                return jsonify({
                    'success': True,
                    'business': [business.long()]
                    'posts': current_posts
                }), 200

            except Exception as e:
                print(e)
                abort(404)

        return get_business_detail()

    if requires.method == 'PATCH':
        @requires_auth('patch:business')
        def update_business(payload, bus_id):
            '''Updates business by ID'''
            try:
                business = Business.query.filter(Business.id == bus_id).first()
                business.name = reqest.json.get('name')
                business.phone = request.json.get('phone')
                business.description = request.json.get('description')

                selection = business.posts.order_by(
                    Post.timestamp.desc()).all()
                current_posts = paginate_posts(request, selection)

                business.update()

                return jsonify({
                    'success': True,
                    'business': [business.long()],
                    'posts': current_posts
                })

            except Exception as e:
                print(e)
                abort(404)

        return update_business()

    if request.method == 'DELETE':
        @requires_auth('delete:business')
        def delete_business(payload, bus_id):
            '''Deletes business by ID'''
            try:
                business = Business.qeury.filter(Business.id == bus_id).first()
                business.delete()

                return jsonify({
                    'success': True,
                    'delete': business.id
                }), 200

            except Exception as e:
                print(e)
                abort(404)

        return delete_business()

# ---------------------------------------------------------------
# Posts Routes
# ---------------------------------------------------------------
