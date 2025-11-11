from flask import Flask, render_template, request, redirect, flash, session
import sqlite3
from hashlib import sha512
from functools import wraps

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = "hdkjhdkjfhkdshfdjkshfdksjfhdskjfhdskjhfdskhfds"

def get_db_cursor():
    db = sqlite3.connect('crm.db')
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    return cursor

con = sqlite3.connect('crm.db')
cursor = con.cursor()
cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    username TEXT UNIQUE NOT NULL, 
                    password TEXT NOT NULL,
                    role TEXT, 
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
               """)


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



@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=[ 'GET', 'POST' ])
def login():
    username = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed = sha512((username + password).encode('utf-8')).hexdigest()
        cursor = get_db_cursor()
        user = cursor.execute("SELECT * FROM users WHERE username=? and password=?", (username, hashed)).fetchone()
        if user:
            # Save user data in session
            session['uid'] = user['id']
            session['role'] = user['role']
            role = user['role']
            if role == 'admin':
                return redirect('/admin')
            elif role == 'employee':
                return redirect('/employee')
            elif role == 'manager':
                return redirect('/manager')
            else:
                flash('User has an invalid role')
        else:
            flash('Invalid credentials')
    return render_template('login.html', username=username)


@app.route('/employee')
@roles_permitted(['employee', 'admin'])
def employee():
    return render_template('employee.html')


@app.route('/manager')
@roles_permitted(['manager'])
def manager():
    return render_template('manager.html')


@app.route('/admin')
@roles_permitted(['admin'])
def admin():
    return render_template('admin.html')



@app.route('/logout')
def logout():
    session.clear()
    flash('Succesfully logged out')
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)