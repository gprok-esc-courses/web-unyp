from flask import Flask, render_template, request, redirect, session
import sqlite3
import hashlib
import bcrypt

app = Flask(__name__)
app.secret_key = "sdfsdlkfhjsdlfjhsdlkflfdshfdsklhfkjlhiodsfhsiofhiofdshfoisfhjoishodi"

conn = sqlite3.connect("store.db")
cursor = conn.cursor()
cursor.execute("""
               CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL
               )
               """)
cursor.execute("""
               CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
               )
               """)
conn.commit()
conn.close()



@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form 
        db = sqlite3.connect("store.db")
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        user = cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (data['username'], data['password'])).fetchone()
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return "USER OK"
        else:
            session.clear()
            return "WRONG CREDENTIALS"
    return render_template('login.html')

@app.route('/products')
def products():
    product_list = [
        {'name': 'Monitor XA56', 'price': 176.2},
        {'name': 'Monitor KQW2', 'price': 565.7},
        {'name': 'Keyboard N1', 'price': 44.9},
        {'name': 'Keyboard KPO89', 'price': 78.1},
    ]
    return render_template('products.html', products=product_list)

@app.route('/products/db')
def products_db():
    db = sqlite3.connect("store.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    product_list = cursor.execute("SELECT * FROM products").fetchall()
    return render_template('products.html', products=product_list)

@app.route('/product/add', methods=['POST'])
def product_add():
    data = request.form
    
    db = sqlite3.connect("store.db")
    cursor = db.cursor()
    cursor.execute("INSERT INTO products (name, price) VALUES (?, ?)", (data['product_name'], data['price']))
    db.commit()
    db.close()

    return redirect('/products/db')

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/protected')
def protected():
    if 'username' in session:
        return "WELOCME " + session['username']
    else:
        return "This page is protected, please login"
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/test/hash', methods=['GET', 'POST'])
def test_hash():
    if request.method == 'POST':
        password = request.form['password'] 
        hashed = hashlib.sha512(password.encode()).hexdigest()
        return f"Password {password}, <br>Hashed password: {hashed}"
    else:
        return render_template('test_hash.html')
    

@app.route('/test/bcrypt/hash', methods=['GET', 'POST'])
def test_bcrypt_hash():
    if request.method == 'POST':
        password = request.form['password'].encode()
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password, salt)
        hasheed = hashed_password.decode()
        return f"Password {password}, <br>Hashed password: {hashed_password}"
    else:
        return render_template('test_bcrypt.html')
        



if __name__ == '__main__':
    app.run(debug=True)


