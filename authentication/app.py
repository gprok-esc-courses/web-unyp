from flask import Flask, render_template, request, redirect, flash, session
import sqlite3
from hashlib import sha512

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
def employee():
    if 'role' in session and session['role'] == 'employee':
        return render_template('employee.html')
    else:
        flash('Invalid role to access this page')
        return redirect('/login')


@app.route('/manager')
def manager():
    if 'role' in session and session['role'] == 'manager':
        return render_template('manager.html')
    else:
        flash('Invalid role to access this page')
        return redirect('/login')


@app.route('/admin')
def admin():
    if 'role' in session and session['role'] == 'admin':
        return render_template('admin.html')
    else:
        flash('Invalid role to access this page')
        return redirect('/login')


@app.route('/logout')
def logout():
    session.clear()
    flash('Succesfully logged out')
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)