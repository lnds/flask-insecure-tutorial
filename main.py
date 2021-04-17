# warning this project has vulnerabilites on purpose
import sqlite3
import html
from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

def get_db_connection():
  conn = sqlite3.connect('database.db')
  conn.row_factory = sqlite3.Row
  return conn

def get_post(post_id):
  conn = get_db_connection()
  post = conn.execute(f"SELECT * FROM posts WHERE ID = {post_id}").fetchone()
  conn.close()
  if post is None:
    abort(404)
  return post

@app.route('/')
def index():
  conn = get_db_connection()
  posts = conn.execute('SELECT * FROM posts').fetchall()
  conn.close()
  return render_template('index.html', posts=posts)

@app.route('/<int:post_id>')
def post(post_id):
  post = get_post(post_id)
  return render_template('post.html', post=post)


@app.route('/add')
def add():
  return render_template('formulario.html', action='/create', label='Escribe', post=None)


@app.route('/create')
def create():
  title = request.args.get('title')
  title = html.unescape(title)
  print('title = ', title)
  content = request.args.get('content')
  content = html.unescape(content)
  
  if not title:
    flash('Se requiere un titulo al menos', 'danger')
  else:
    conn = get_db_connection()
    conn.execute(f"INSERT INTO posts(title, content) VALUES('{title}', '{content}')")
    conn.commit()
    conn.close()
    flash('Post creado', 'success')
    return redirect(url_for('index'))

  return render_template('formulario.html', action='/create', post=None)

@app.route('/<int:id>/edit')
def edit(id):
  post = get_post(id)
  return render_template('formulario.html', action='/save', post=post, label='Modifica')
  
  
  
app.run(host='0.0.0.0', port=8080)