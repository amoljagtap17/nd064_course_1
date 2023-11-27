import sqlite3

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort

import logging
import sys

# custom logger configuration
logger=logging.getLogger('app')
log_format='INFO:%(name)s:%(asctime)s, %(message)s'
date_format='%m/%d/%Y, %H:%M:%S'

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=log_format, datefmt=date_format)

# Total amount of connections to the database
db_connection_count = 0

# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    global db_connection_count
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    db_connection_count += 1
    return connection

# Function to close a database connection.
def close_db_connection(connection):
    global db_connection_count
    connection.close()
    # commenting below line as the count is always reset to 0
    # db_connection_count -= 1

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    close_db_connection(connection)
    return post

# Function to get all posts
def get_posts():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    close_db_connection(connection)
    return posts

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application 
@app.route('/')
def index():
    posts = get_posts()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      return render_template('404.html'), 404
    else:
      logger.info('Article "{0}" retrieved!'.format(post['title']))
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            close_db_connection(connection)

            return redirect(url_for('index'))

    return render_template('create.html')

# Healthcheck endpoint
@app.route('/healthz')
def healthcheck():
    response = app.response_class(
            response=json.dumps({"result": "OK - healthy"}),
            status=200,
            mimetype='application/json'
    )
    return response

# Metrics endpoint
@app.route('/metrics')
def metrics():
    posts = get_posts()
    response = app.response_class(
            response=json.dumps({"status":"success","code":0,"data":{"db_connection_count": db_connection_count, "post_count": len(posts)}}),
            status=200,
            mimetype='application/json'
    )
    return response

# start the application on port 3111
if __name__ == "__main__":
   app.run(host='0.0.0.0', port='3111')
