import mysql.connector
import base64
import bcrypt

def mysql_connection():
    db = mysql.connector.connect(
            host = '130.61.177.13',
            port = '3306',
            user = 'evoting',
            password = 'TzC95k3Z6eg5SRGHgtcqOCP7',
            database = 'evoting',
            connection_timeout=180
    )
    c = db.cursor()
    return c, db

def create_user(pesel, password):
    password_salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password.encode(), password_salt)
    c, db = mysql_connection()
    c.execute(f"INSERT INTO users (pesel, salt, password) VALUES (\"{pesel}\", \"{base64.b64encode(password_salt)}\", \"{base64.b64encode(password_hash)}\");")
    db.commit()
    db.close()

def verify_user(pesel, password):
    c, db = mysql_connection()
    c.execute(f"SELECT * FROM users WHERE pesel=\"{pesel}\";")
    user = c.fetchone()
    if not user: return False

    password_salt = base64.b64decode(user[2][2:-1])
    password_hash = bcrypt.hashpw(password.encode(), password_salt)
    
    if str(base64.b64encode(password_hash)) == user[3]:
        return True
    else:
        return False

"""
create_user('01234567890', 'password0')
create_user('01234567891', 'password1')
create_user('01234567892', 'password2')
create_user('01234567893', 'password3')
create_user('01234567894', 'password4')
create_user('01234567895', 'password5')
create_user('01234567896', 'password6')
create_user('01234567897', 'password7')
create_user('01234567898', 'password8')
create_user('01234567899', 'password9')
print(verify_user('01234567893', 'password3'))
"""