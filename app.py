from flask import Flask, render_template, request, redirect, url_for, flash 
import psycopg2
import os

app = Flask(__name__)

app.secret_key = os.urandom(24)

tasks = ['description', 'Date', 'comment']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(len(username))
        if len(username) < 3:
            flash("Username must be at least 3 characters long", "error")
            print('hhff')
            return render_template('register.html', errors='Username must be at least 3 characters long')
        try:
            conn = psycopg2.connect(
                    database='flask',
                    user='postgres',
                    password='060101',
                    port=5432
                )
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            existing_user = cursor.fetchone()
            print('dcdhcush')
            if existing_user:
                        flash("Username already exists. Please choose a different one.", "error")
                        return redirect(url_for('register'))

            cursor.execute("""
                insert into users(id, username, password) values (1, 'user', 'user')
            """)
            conn.commit()
            conn.close()

            flash("Registration successful!", "success")
            return redirect(url_for('login'))
        except Exception as e:
            flash(f"Error connecting to the database: {e}", "error")

    return render_template('register.html')

    

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/task_index')
def task():
    return render_template('task_index.html')

@app.route('/add_task', methods=['POST'])
def add_task():
    task = request.form['task']
    print("gfgbgbgbgbgbgbfgb", task)
    tasks.append(task) 
    return redirect('/')  

@app.route('/delete_task', methods=['POST'])
def delete_task():
    task = request.form['task']  
    if task in tasks:
        tasks.remove(task)  
    return redirect('/')  

if __name__ == '__main__':
    app.run(debug=True)
