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
    # Store data in Redis
    for key, value in data.items():
        redis_db.set(key, value)
    return jsonify(success=True)

##getot za prikazhuvanje na datata
@app.route('/')
def index():
    data = {key.decode('utf-8'): redis_db.get(key).decode('utf-8') for key in redis_db.keys()}

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
                <th>Value</th>
            </tr>
            {% for key, value in data.items() %}
            <tr>
                <td>{{ key }}</td>
                <td>{{ value }}</td>
            </tr>
            {% endfor %}
        </table>     
    </body>
    </html>
    """, data=data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

