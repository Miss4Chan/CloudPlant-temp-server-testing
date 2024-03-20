from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Temporary storage for received data
received_data = {}

@app.route('/data', methods=['POST'])
def receive_data():
    global received_data
    data = request.json
    received_data = data
    return jsonify(success=True)

@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sensor Data</title>
    </head>
    <body>
        <h1>Received Sensor Data</h1>
        <p>Device ID: {{ data.get('deviceID', 'N/A') }}</p>
        <p>Light Intensity: {{ data.get('lightIntensity', 'N/A') }}</p>
        <p>Temperature: {{ data.get('temperature', 'N/A') }}°C</p>
        <p>Humidity: {{ data.get('humidity', 'N/A') }}%</p>
    </body>
    </html>
    """, data=received_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

