import psycopg2
import config


connection = psycopg2.connect(
   host=config.host,
   database=config.database,
   user=config.user,
   password=config.password,
)
    
exists = False




with connection.cursor() as cur:
   cur.execute("select exists(select relname from pg_class where relname='posts')")
   exists = cur.fetchone()[0]
   
   if not exists:
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