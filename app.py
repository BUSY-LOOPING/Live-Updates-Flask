from gevent import monkey
monkey.patch_all()
from gevent.pywsgi import WSGIServer
from flask import Flask, render_template, Response, stream_with_context
import json
import time
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL, MySQLdb
from random import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/test'
db = SQLAlchemy(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'test'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

counter = 100

@app.route('/')
def index() :
    # cursor = mysql.connection.cursor()
    # cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # cur.execute('SELECT * FROM todo')
    # webframework = cur.fetchall()
    # return render_template('index.html', webframework = webframework)
    return render_template('index.html')
    
@app.route('/new')
def new() :
    return 'new'

@app.route('/listen')
def listen():
    def respond_to_client() :
        while True:
            global counter
            with open('color.txt', 'r') as f:
                color = f.read()
                print('*********')
                if (color != 'white') :
                    print(counter)
                    counter = random()
                    _data = json.dumps({'color' : color, 'counter': counter})
                    yield f"id :1\ndata: {_data}\nevent: online\n\n"
                time.sleep(0.5)
    return Response(respond_to_client(), mimetype='text/event-stream')

if __name__ == '__main__' :
    # app.run(host='0.0.0.0',debug=True, port=5000)
    http_server = WSGIServer(('0.0.0.0', 80), app)
    http_server.serve_forever()
        