    # from flask import Flask, render_template, request, redirect, url_for, flash, session
    # import psycopg2
    # import os
    # import hashlib

    # app = Flask(__name__)
    # app.secret_key = os.urandom(24)

    # # Функция для подключения к базе данных
    # def get_db_connection():
    #     return psycopg2.connect(
    #         database='flask',
    #         user='postgres',
    #         password='060101',
    #         port=5432
    #     )

    # # Главная страница с задачами
    # @app.route('/')
    # def index():
    #     if 'user_id' not in session:
    #         return redirect(url_for('login'))  # Перенаправление на страницу входа

    #     conn = get_db_connection()
    #     cursor = conn.cursor()

    #     cursor.execute("SELECT * FROM tasks WHERE user_id = %s", (session['user_id'],))
    #     tasks = cursor.fetchall()

    #     conn.close()
    #     return render_template('index.html', tasks=tasks)

    # # Регистрация пользователя
    # @app.route('/register', methods=['GET', 'POST'])
    # def register():
    #     if request.method == 'POST':
    #         username = request.form['username']
    #         password = request.form['password']

    #         # Проверка длины имени пользователя
    #         if len(username) < 3:
    #             flash("Username must be at least 3 characters long", "error")
    #             return render_template('register.html', errors='Username must be at least 3 characters long')

    #         # Хеширование пароля
    #         hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    #         try:
    #             conn = get_db_connection()
    #             cursor = conn.cursor()

    #             # Проверка, существует ли уже такой пользователь
    #             cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    #             existing_user = cursor.fetchone()

    #             if existing_user is not None:
    #                 flash("Username already exists. Please choose a different one.", "error")
    #                 return redirect(url_for('register'))

    #             # Вставка нового пользователя в базу данных
    #             cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
    #             conn.commit()

    #             # Сохранение в сессии данных пользователя
    #             session['username'] = username

    #             conn.close()

    #             flash("Registration successful! Welcome, {}".format(username), "success")
    #             return redirect(url_for('index'))  # Перенаправление на главную страницу после регистрации

    #         except Exception as e:
    #             flash(f"Error connecting to the database: {e}", "error")
    #             return render_template('register.html')

    #     return render_template('register.html')

    # # Вход пользователя
    # @app.route('/login', methods=['GET', 'POST'])
    # def login():
    #     if request.method == 'POST':
    #         username = request.form['username']
    #         password = request.form['password']

    #         # Хеширование пароля
    #         hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    #         conn = get_db_connection()
    #         cursor = conn.cursor()

    #         cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, hashed_password))
    #         user = cursor.fetchone()

    #         if user:
    #             # Сохранение user_id в сессии после успешного входа
    #             session['user_id'] = user[0]
    #             flash("Login successful!", "success")
    #             return redirect(url_for('index'))
    #         else:
    #             flash("Invalid username or password.", "error")
    #             return redirect(url_for('login'))

    #     return render_template('login.html')

    # @app.route('/delete_user', methods=['POST'])
    # def delete_user():

    #     if 'user_id' not in session:
    #         flash("You must be logged in to delete your account.", "error")
    #         return redirect(url_for('login'))

    #     try:
    #         user_id = session['user_id']
    #         conn = get_db_connection()
    #         cursor = conn.cursor()

    #         cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    #         conn.commit()

    #         cursor.execute("DELETE FROM tasks WHERE user_id = %s", (user_id,))
    #         conn.commit()

    #         conn.close()

    #         session.pop('user_id', None)
    #         session.pop('username', None)

    #         flash("Your account has been deleted successfully.", "success")
    #         return redirect(url_for('index'))  
    #     except Exception as e:
    #         flash(f"Error deleting your account: {e}", "error")
    #         return redirect(url_for('index'))

    # @app.route('/add_task', methods=['POST'])
    # def add_task():
    #     if 'user_id' not in session:
    #         return redirect(url_for('login'))  
    #     description = request.form['description']
    #     due_date = request.form['due_date']

    #     conn = get_db_connection()
    #     cursor = conn.cursor()

    #     cursor.execute("INSERT INTO tasks (user_id, description, due_date) VALUES (%s, %s, %s)",
    #                    (session['user_id'], description, due_date))
    #     conn.commit()
    #     conn.close()

    #     flash("Task added successfully!", "success")
    #     return redirect(url_for('index'))

    # @app.route('/delete_task', methods=['POST'])
    # def delete_task():
    #     if 'user_id' not in session:
    #         return redirect(url_for('login'))  # Перенаправление на страницу входа

    #     task_id = request.form['task_id']  # Получаем task_id из формы

    #     conn = get_db_connection()
    #     cursor = conn.cursor()

    #     cursor.execute("DELETE FROM tasks WHERE id = %s AND user_id = %s", (task_id, session['user_id']))
    #     conn.commit()
    #     conn.close()


        
    #     flash("Task deleted successfully!", "success")
    #     return redirect(url_for('index'))

    # if __name__ == '__main__':
    #     app.run(debug=True)

# import psycopg2

# conn = psycopg2.connect(
#     database='flask',
#     user='postgres',
#     password='060101',
#     port=5432
# )

# cursor = conn.cursor()

# cursor.execute("""
#     insert into users(id, username, password) values (1, 'user', 'user')
# """)
# conn.commit()
# conn.close()

login = "asd"
password = "asd"
print("LOGIN = %s AND PASSWORD = %s"%(login, password))