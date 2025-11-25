from flask import Flask, request, render_template, redirect, flash, session
import sqlite3 
from hashlib import sha512
from functools import wraps

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = "lasdlaisdhsalkdhsaohsalashdioasdhsaiodhoaidfhwefhoweifoiweoifhweofehfewpoih"


def roles_permitted(roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if 'uid' in session:
                if session['role'] in roles:
                    return f(*args, **kwargs)
                else:
                    flash('ERROR: your role has no access to this page')
                    return redirect('login')
            else:
                flash('ERROR: you need to login')
                return redirect('login')
        return wrapper
    return decorator


def get_db_conn():
    db = sqlite3.connect('projects.db')
    db.row_factory = sqlite3.Row
    return db 


def initialize_db():
    db = get_db_conn()
    cursor = db.cursor()

    # Users table 
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        username TEXT UNIQUE NOT NULL, 
                        password TEXT NOT NULL, 
                        role TEXT DEFAULT 'user',
                        blocked INTEGER DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                   """)

    # Projects table 
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS projects (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        title TEXT NOT NULL,
                        archived INTEGER DEFAULT 0,
                        user_id INTEGER NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                   """)

    # Tasks table
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        name TEXT NOT NULL,
                        due TEXT, 
                        completed INTEGER DEFAULT 0,
                        project_id INTEGER NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (project_id) REFERENCES projects (id)
                    )
                   """)
    
    db.commit()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register', methods=[ 'GET', 'POST' ])
def register():
    username = ''
    if request.method == 'POST':
        data = request.form 
        username = data['username']
        password = data['password']
        password2 = data['password2']
        if password == password2:
            db = get_db_conn()
            cursor = db.cursor()
            user = cursor.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
            if not user:
                hashed = sha512((username + password).encode('utf-8')).hexdigest()
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
                db.commit()
                return redirect('/login')
            else:
                flash('ERROR: Username already taken')
        else:
            flash('ERROR: Passwords do not match')
    return render_template('register.html', username=username)


@app.route('/login', methods=[ 'GET', 'POST' ])
def login():
    username = ''
    if request.method == 'POST':
        data = request.form 
        username = data['username']
        password = data['password']
        db = get_db_conn()
        cursor = db.cursor()
        user = cursor.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
        if user:
            hashed = sha512((username + password).encode('utf-8')).hexdigest()
            if hashed == user['password']:
                session['uid'] = user['id']
                session['username'] = user['username']
                session['role'] = user['role']
                if user['role'] == 'user':
                    return redirect('/projects')
                else:
                    return redirect('/dashboard')
            else:
                flash("ERROR: Wrong credentials")
        else:
            flash("ERROR: Username not found")
    return render_template('login.html', username=username)


@app.route('/projects')
@roles_permitted(['user'])
def projects():
    db = get_db_conn()
    cursor = db.cursor()
    uid = session['uid']
    all_projects = cursor.execute("SELECT * FROM projects WHERE user_id=?", (uid,)).fetchall() 
    return render_template('projects.html', projects=all_projects)



@app.route('/dashboard')
@roles_permitted(['admin'])
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("INFO: You have been logged out")
    return redirect('/login')


@app.route('/add/project', methods=[ 'GET', 'POST' ])
@roles_permitted(['user'])
def add_project():
    if request.method == 'POST':
        data = request.form 
        title = data['title']
        uid = session['uid']
        db = get_db_conn()
        cursor = db.cursor()
        cursor.execute("INSERT INTO projects (title, user_id) VALUES (?, ?)", (title, uid))
        db.commit()
        return redirect('/projects')
    else:
        return render_template('add_project.html')



if __name__ == '__main__':
    initialize_db()
    app.run(debug=True)



