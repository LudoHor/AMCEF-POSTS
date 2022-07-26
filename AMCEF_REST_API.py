from email import message
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_restful import abort
import requests
from flask_expects_json import expects_json
from models import *


def bad_request(message):
    response = jsonify({'message': message})
    response.status_code = 403
    return response


@app.route('/')
def hello():
    """REST API DEFAULT PAGE


    """

    return 'AMCEF REST API'


@app.route('/rest_posts', methods=['GET'])
@app.output(PostOutSchema(many=True))
def REST_posts():
    """Get all posts

    Return all the post in databse
    """

    posts = Post.query.all()
    return jsonify([post.to_json() for post in posts])


@app.route('/rest_posts_user_id/<int:userId>', methods=['GET'])
@app.output(PostOutSchema(many=True))
def REST_posts_user_id(userId):
    """Get post by user

    Return all the post for selected user
    """
    data = Post.query.filter_by(userId=userId).all()
    return jsonify([post.to_json() for post in data])


@app.route('/rest_posts_post_id/<int:pId>', methods=['GET'])
@app.output(PostOutSchema)
def REST_posts_post_id(pId):
    """Get post by post ID

    Return post from databes based on ID
    """
    data = Post.query.filter_by(id=pId).first()
    if(not data):
        resp = requests.get(
            "https://jsonplaceholder.typicode.com/posts/{}".format(pId))
        post = resp.json()
        if (post):
            my_data = Post(post['id'], post['userId'],
                           post['title'], post['body'])
            db.session.add(my_data)
            db.session.commit()
            return my_data.to_json()
        return post

    return data.to_json()


@app.route('/rest_create_post', methods=['POST'])
@app.input(PostInSchema)
@app.output(PostOutSchema)
def REST_create_post(data):
    """Create post

    Create new post in database
    """
    if request.method == 'POST':
        resp = requests.get("https://jsonplaceholder.typicode.com/users")
        users = resp.json()

        resp2 = requests.get("https://jsonplaceholder.typicode.com/posts")
        exist_posts = resp2.json()

        post = data

        if(post['userId'] not in [i['id'] for i in users]):
            return bad_request("User doesn't exist")

        if(post['id'] in [i['id'] for i in exist_posts]):
            return bad_request('Post already exists')

        if(Post.query.filter_by(id=post['id']).first()):
            return bad_request('Post already exists')

        my_data = Post(post['id'], post['userId'], post['title'], post['body'])
        db.session.add(my_data)
        db.session.commit()

        return my_data.to_json()


@app.route('/rest_update_post/<int:pId>', methods=['PUT'])
@app.input(PostUpdateInSchema)
@app.output(PostOutSchema)
def REST_update_post(pId, post_data):
    """Update post

    Update post title and body
    """
    if request.method == 'PUT':
        post = post_data

        data = Post.query.filter_by(id=pId).first_or_404()

        data.body = post['body']
        data.title = post['title']
        db.session.commit()

        return data.to_json()


@app.route('/rest_delete_post/<int:pId>', methods=['DELETE'])
def REST_delete_post(pId):
    """Delete post

    Delete post by id
    """
    if request.method == 'DELETE':

        data = Post.query.filter_by(id=pId).first_or_404()
        db.session.delete(data)
        db.session.commit()

        return data.to_json()


if __name__ == '__main__':

    app.run(debug=True)
