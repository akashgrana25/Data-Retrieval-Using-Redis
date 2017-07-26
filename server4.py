import redis
from flaskext.mysql import MySQL
from flask import Flask, render_template
import time
import random

from flask import Flask
app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'akashdb25'
app.config['MYSQL_DATABASE_PASSWORD'] = 'akashdb25'
app.config['MYSQL_DATABASE_DB'] = 'akashdb25'
app.config['MYSQL_DATABASE_HOST'] = 'akashdb1025.cnjdofsvvuyc.us-west-2.rds.amazonaws.com'
mysql.init_app(app)

conn = mysql.connect()
cursor =conn.cursor()

@app.route("/")
def main():
    return render_template('Index.html')


@app.route('/execution_time', methods=['POST'])
def execution_time():
    start_time = time.time()
    end_time = ''
        # var_val = random(5000)
    for i in range(0,50):
        var_val = random.randint(0, 200)

        cursor.execute("SELECT * from DEATH where plus_65_years = %s " %var_val)
        data = cursor.fetchall()
        # print data
    end_time = time.time() - start_time

    return render_template('Index.html', data = end_time)



@app.route('/redis_time', methods=['POST'])
def redis_time():
    r = redis.StrictRedis(host='akashdb25.fqxtdn.0001.usw2.cache.amazonaws.com', port=6379, db=0)

    start_time = time.time()
    end_time = ''
    for i in range(0, 50):
        var_val = random.randint(0, 200)
        query_str = "SELECT * from DEATH where plus_65_years = %s " % var_val
        exist = r.get(query_str)
        if exist:
            # print "Query exists"
            continue
        else:
            cursor.execute(query_str)

            data = cursor.fetchall()
            set_cache = r.set(query_str,data)
            # print data
    end_time = time.time() - start_time

    return render_template('Index.html', result=end_time)

@app.route('/table_data', methods=['POST'])
def table_data():
    for i in range(0,50):
        var_val = random.randint(0, 200)

        cursor.execute("SELECT * from DEATH where plus_65_years = %s " %var_val)
        data = cursor.fetchall()
        temp = ''
        for iter in data:
            temp = temp + str(iter)

        #return render_template('Index.html', table=data)
        return render_template('Index.html', item = data)




if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8080, debug=True)
    app.run(host='0.0.0.0', debug=True)