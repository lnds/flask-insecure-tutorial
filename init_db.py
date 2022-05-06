import psycopg2

connection = psycopg2.connect(
    host="db",
    database="flask_db",
    user="user",
    password="pass"
  )


with connection.cursor() as cur:
    cur.execute(open('schema.sql', 'r').read())

    cur.execute("INSERT INTO posts (title, content) VALUES (%s, %s)",
            ('First Post', 'Content for the first post')
            )

    cur.execute("INSERT INTO posts (title, content) VALUES (%s, %s)",
            ('Second Post', 'Content for the second post')
            )
    cur.close()

connection.commit()
connection.close()