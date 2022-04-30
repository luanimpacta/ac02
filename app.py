from flask import Flask, render_template, request
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'NpmFmMxjmSXk46k'
app.config['MYSQL_DATABASE_DB'] = 'ac02'
app.config['MYSQL_DATABASE_HOST'] = '172.17.0.2'
mysql.init_app(app)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/signup', methods=['POST', 'GET'])
def post():
    try:
        _name = request.form['name']
        _email = request.form['email']
        _address = request.form['address']

        if _name and _address and _email:
            conn = mysql.connect()
            cursor = conn.cursor()

            sql = "INSERT INTO tb_users(name, email, address) VALUES (%s, %s, %s)"
            value = (_name, _email, _address)

            cursor.execute(sql, value)
            conn.commit()

    except Exception as e:
        print("Problem inserting into db: " + str(e))
    finally:
        return render_template('index.html')


@app.route('/list', methods=['POST', 'GET'])
def index():
    conn = mysql.connect()
    cursor = conn.cursor()

    query = 'SELECT name, email, address FROM tb_users'
    cursor.execute(query)

    data = cursor.fetchall()

    return render_template('list.html', data=data)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5001)
