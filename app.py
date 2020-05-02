import os
from flask import Flask, request, abort, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)

    @app.route('/', methods=['GET'])
    def index():
        '''Shows all posts from businesses (News, Etc)'''
        try:
            return render_template('index.html'), jsonify({
                'success': True,
                'posts': [post.short() for post in Post.query.all()]
            }), 200
        except Exception as e:
            print(e)
            abort(404)

    @app.route('/directory', methods=['GET', 'POST'])
    if request.method == 'GET':
        def directory():
            '''Shows all listed businesses'''
            return render_template('directory.html', title='Business Directory',
                                businesses=businesses.items)
    if request.method == 'POST':
        def create_listing():
            try:
                listing = Business(
                    title=request.json['name'],
                    post
                )

    @app.route('/directory/<bus_id>', methods=['GET', 'PATCH', 'DELETE'])
    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
