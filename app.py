from flask import Flask, render_template, request, redirect, url_for, flash, session
import psycopg2
import os
import hashlib

app = Flask(__name__)
app.secret_key = os.urandom(24)

def get_db_connection():
    return psycopg2.connect(
        database='flask',
        user='postgres',
        password='060101',
        port=5432
    )

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    print("FFFFFF:", session['user_id'])

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks WHERE user_id = %s", (session['user_id'],))
    tasks = cursor.fetchall()

    conn.close()    
    return render_template('index.html', tasks=tasks)

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
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        
        try:    
            conn = get_db_connection()
            if conn is None:
                flash("Error connecting to the database", "error")
                return redirect(url_for('register'))
            cursor = conn.cursor()

            print("Username:", username)
            print("Hashed Password:", hashed_password)

        
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            existing_user = cursor.fetchone()
            print('dcdhcush', existing_user, "AAAAAAAAAAAAAA")
            if existing_user is not None:
                flash("Username already exists. Please choose a different one.", "error")
                return redirect(url_for('register'))

            cursor.execute("""
                INSERT INTO users (username, password) VALUES (%s, %s)
            """, (username, hashed_password))
            conn.commit()

            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))

            user = cursor.fetchone()
            session['user_id'] = user[0]  
            session['username'] = username  

            conn.close()

            flash("Registration successful! Welcome, {}".format(username), "success")
            return redirect(url_for('index'))  

        except Exception as e:
            flash(f"Error connecting to the database: {e}", "error")
            return render_template('register.html')
    
    return render_template('register.html')
        
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        conn = get_db_connection()
        cursor = conn.cursor()  

        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, hashed_password))
        user = cursor.fetchone()
        print("USER: ",user)
        if user:
            session['user_id'] = user[0] 
            session['username'] = username  
            flash("Login successful!", "success")
            return redirect(url_for('index'))  
        else:
            flash("Invalid username or password.", "error")
            return redirect(url_for('login'))
    return render_template('login.html')

    #     if user:
    #         session['user_id'] = user[0]  
    #         flash("Login successful!", "success")
    #         return redirect(url_for('index'))
    #     else:
    #         flash("Invalid username or password.", "error")
    #         return redirect(url_for('login'))

    # return render_template('login.html')
  

@app.route('/task_index')
def task():
    tasks = task.query.all()  
    return render_template('task_index.html', tasks=tasks)
    
@app.route('/add_task_page', methods=['GET', 'POST'])
def add_task_page():
    if request.method == 'POST':
        description = request.form.get('description')
        due_date = request.form.get('due_date')
        comment = request.form.get('comment')

        if not description or not due_date or not comment:
            flash("All fields must be filled in", "error")
            return redirect(url_for('add_task_page'))  
        
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO tasks (user_id, description, due_date, comment)
            VALUES (%s, %s, %s, %s)
        """, (session['user_id'], description, due_date, comment))
        conn.commit()
        conn.close()

        flash("Task added successfully!", "success")
        return redirect(url_for('index'))  
    
    return render_template('add_task.html')  

@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    if 'user_id' not in session:
        return redirect(url_for('login'))  

    description = request.form.get('description')
    due_date = request.form.get('due_date')
    comment = request.form.get('comment')

    if not description or not due_date or not comment:
        flash("All fields must be filled in", "error")
        return redirect(url_for('add_task_page'))  
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO tasks (user_id, description, due_date, comment) VALUES (%s, %s, %s, %s)", 
                   (session['user_id'], description, due_date, comment))
    conn.commit()
    conn.close()

    flash("Task added successfully!", "success")
    return redirect(url_for('index'))  

    
@app.route('/delete_task', methods=['GET', 'POST'])
def delete_task():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    task_id = request.form['task_id']  
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id = %s AND user_id = %s", (task_id, session['user_id']))
    conn.commit()
    conn.close()

    flash("Task deleted successfully!", "success")
    return redirect(url_for('index'))

@app.route('/delete_user_by_username', methods=['POST'])
def delete_user_by_username():
    if 'user_id' not in session:
        flash("You must be logged in to delete users.", "error")
        return redirect(url_for('login'))

    username_to_delete = request.form['username']  

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM users WHERE username = %s", (username_to_delete,))
        conn.commit()

        flash(f"User with username {username_to_delete} has been deleted.", "success")
        return redirect(url_for('index'))

    except Exception as e:
        flash(f"Error deleting user: {e}", "error")
        return redirect(url_for('index'))

    finally:
        conn.close()

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)  
    session.pop('username', None)  
    flash("You have successfully logged out of your account.", "success")
    return redirect(url_for('login'))  

if __name__ == '__main__':  
    app.run(debug=True)
