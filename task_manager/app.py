from flask import Flask, request, render_template, redirect, flash
import sqlite3 
from hashlib import sha512

app = Flask(__name__)
app.secret_key = "lasdlaisdhsalkdhsaohsalashdioasdhsaiodhoaidfhwefhoweifoiweoifhweofehfewpoih"

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
    return "HOME PAGE"


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


@app.route('/login')
def login():
    return "LOGIN"





if __name__ == '__main__':
    initialize_db()
    app.run(debug=True)



