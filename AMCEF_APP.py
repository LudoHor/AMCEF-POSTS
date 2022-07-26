from flask import render_template, request, redirect, url_for, flash, jsonify
import requests
from flask_expects_json import expects_json
from models import *


@app.route("/")
@app.route("/index")
def index():
    posts = Post.query.all()
    return render_template("index.html", datas=posts)


@app.route("/add_user", methods=['POST', 'GET'])
def add_user():
    resp = requests.get("https://jsonplaceholder.typicode.com/users")
    user_data = resp.json()
    if request.method == 'POST':
        idf = request.form['id']
        post = requests.get(
            "https://jsonplaceholder.typicode.com/posts/{}".format(idf))
        if(post.json()):
            flash('Post ID already exists', 'danger')
            return render_template("add_user.html", users=user_data)
        userId = request.form['userId']
        title = request.form['title']
        body = request.form['body']

        my_data = Post(idf, userId, title, body)
        db.session.add(my_data)
        db.session.commit()

        flash('User Added', 'success')
        return redirect(url_for("index"))

    return render_template("add_user.html", users=user_data)


@app.route("/edit_user/<string:uid>", methods=['POST', 'GET'])
def edit_user(uid):
    data = Post.query.filter_by(pk_id=uid).first()
    if request.method == 'POST':

        title = request.form['title']
        body = request.form['body']
        data.body = body
        data.title = title
        db.session.commit()

        flash('User Updated', 'success')

        return render_template("index.html", datas=[data])

    return render_template("edit_user.html", datas=data)


@app.route("/delete_user/<string:uid>", methods=['GET'])
def delete_user(uid):
    my_data = Post.query.get(uid)
    db.session.delete(my_data)
    db.session.commit()
    flash('User Deleted', 'warning')
    return redirect(url_for("index"))


@app.route('/search_user_id', methods=['GET'])
def seach_user_id():
    userId = request.args.get("userId")

    data = Post.query.filter_by(userId=userId).all()

    return render_template("index.html", datas=data)


@app.route('/search_post_id', methods=['GET'])
def seach_post_id():
    pId = request.args.get("pId")
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
            return render_template("index.html", datas=[my_data])
        return render_template("index.html", datas=[])

    return render_template("index.html", datas=[data])


if __name__ == '__main__':

    app.run(debug=True)
