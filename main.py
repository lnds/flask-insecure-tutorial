# warning this project has vulnerabilites on purpose
import html
import os
from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
import psycopg2
import psycopg2.extras


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

nombre_blog = os.environ.get('TITULO', default='')

def get_db_connection():
  conn = psycopg2.connect(
    host="db",
    database="flask_db",
    user="user",
    password="pass"
  )
  return conn

def get_post(post_id):
  conn = get_db_connection()
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  cur.execute(f"SELECT * FROM posts WHERE ID = {post_id}")
  post = cur.fetchone()
  cur.close()
  conn.close()
  if post is None:
    abort(404)
  return post

@app.route('/')
def index():
  conn = get_db_connection()
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  cur.execute('SELECT * FROM posts')
  posts = cur.fetchall()
  cur.close()
  conn.close()
  return render_template('index.html', posts=posts, nombre_blog=nombre_blog)

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
    cur = conn.cursor()
    cur.execute(f"INSERT INTO posts(title, content) VALUES('{title}', '{content}')")
    conn.commit()
    cur.close()
    conn.close()
    flash('Post creado', 'success')
    return redirect(url_for('index'))

  return render_template('formulario.html', action='/create', post=None)

@app.route('/<int:id>/edit')
def edit(id):
  post = get_post(id)
  return render_template('formulario.html', action='/save', post=post, label='Modifica')
  
  
  
app.run(host='0.0.0.0', port=8080)