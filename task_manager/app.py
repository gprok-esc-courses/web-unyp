from flask import Flask
import sqlite3 

app = Flask(__name__)

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



if __name__ == '__main__':
    initialize_db()
    app.run(debug=True)



