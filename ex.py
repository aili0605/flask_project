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