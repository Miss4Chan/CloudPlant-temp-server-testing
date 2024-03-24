from flask import Flask, request, jsonify, render_template_string
import redis

app = Flask(__name__)

#ova e za redisot ideme so default porta 
redis_host = "redis"
redis_port = 6379
redis_db = redis.Redis(host=redis_host, port=redis_port)

## ova e obrabotka na post od microcontroller
@app.route('/data', methods=['POST'])
def receive_data():
    data = request.json
    for key, value in data.items():
        redis_db.rpush(key, value)
        redis_db.ltrim(key, -5, -1)
    return jsonify(success=True)

##getot za prikazhuvanje na datata
@app.route('/')
def index():
    data = {}
    for key in redis_db.keys():
        values = redis_db.lrange(key, -5, -1)
        data[key.decode('utf-8')] = [v.decode('utf-8') for v in values]

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sensor Data</title>
    </head>
    <body>
        <h1>Received Sensor Data</h1>
        <table border="1">
            <tr>
                <th>Field</th>
                <th>Values</th>
            </tr>
            {% for key, values in data.items() %}
            <tr>
                <td>{{ key }}</td>
                <td>{{ values }}</td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """, data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

