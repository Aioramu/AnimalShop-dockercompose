import time
import sqlite3
import redis
from flask import Flask, jsonify,request,render_template

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

#def create_table():
#    conn.cursor().execute("CREATE TABLE IF NOT EXISTS Animals(id integer IDENTITY ,name text NOT NULL,age integer NOT NULL,price NOT NULL,type text NOT NULL,PRIMARY KEY(id));")
#create_table()

#conn=sqlite3.connect('Animal_Shop.db')
#c=conn.cursor()
def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)
def dict_factory(cursor,row):
    d={}
    for idx,col in enumerate(cursor.description):
        d[col[0]]=row[idx]
    return d

@app.route('/')
def hello():
    count = get_hit_count()
    return '{} times.\n'.format(count)
@app.route('/all/')
def get_all():
    conn=sqlite3.connect('Animal_Shop.db')
    c=conn.cursor()
    conn.row_factory=dict_factory
    results=c.execute("SELECT * FROM Animals;").fetchall()
    #results=conn.cursor().fetchall()
    return jsonify(results)
@app.route('/add/',methods=['GET'])
def add():
    conn=sqlite3.connect('Animal_Shop.db')
    c=conn.cursor()
    query=request.args
    id=query.get('id')
    name=query.get('name')
    age=query.get('age')
    price=query.get('price')
    type=query.get('type')
    resp="INSERT INTO Animals(id,name,age,price,type) VALUES("+id+",'"+name+"',"+age+","+price+","+"'"+type+"');"
    #resp="INSERT INTO Animals(name,age,price,type) VALUES('bobby',11,10onn00,cat);"
    c.execute(resp)
    out=c.execute("SELECT * FROM Animals;").fetchall()
    conn.commit()
    return jsonify(out)
@app.route('/buy',methods=['GET'])
def delete():
    conn=sqlite3.connect('Animal_Shop.db')
    query=request.args
    id=query.get('id')
    c=conn.cursor()
    #name=query.get('name')
    #age=query.get('age')
    #price=query.get('price')
    #type=query.get('type')
    resp="DELETE FROM Animals WHERE id="+id+";"
    conn.cursor().execute(resp)
    out=c.execute("SELECT * FROM Animals;").fetchall()
    conn.commit()
    return jsonify(out)
@app.route('/allbytype',methods=['GET'])
def get_type():
    conn=sqlite3.connect('Animal_Shop.db')
    c=conn.cursor()
    query=request.args
    type=query.get('type')
    resp="SELECT * FROM Animals WHERE type='"+type+"';"
    out=c.execute(resp).fetchall()
    return jsonify(out)
@app.route('/change',methods=['GET'])
def change():
    conn=sqlite3.connect('Animal_Shop.db')
    query=request.args
    id=query.get('id')
    name=query.get('name')
    age=query.get('age')
    price=query.get('price')
    type=query.get('type')
    resp="UPDATE Animals SET name='"+name+"',age="+age+",price="+price+",type='"+type+"' WHERE id="+id+";"
    conn.cursor().execute(resp).fetchall()
    out="SELECT * FROM Animals WHERE id="+id+";"
    out=conn.cursor().execute(out).fetchall()
    conn.commit()
    return jsonify(out)
@app.route('/info',methods=['GET'])
def info():
    conn=sqlite3.connect('Animal_Shop.db')
    query=request.args
    id=query.get('id')
    resp="SELECT * FROM Animals WHERE id="+id+";"
    out=conn.cursor().execute(resp).fetchall()
    return jsonify(out)
