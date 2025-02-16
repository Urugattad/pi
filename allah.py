from flask import Flask, request, jsonify, render_template
import random


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('std.html')  # Load the HTML page

@app.route('/toggle_gpio', methods=['POST'])
def submit():
    data = request.get_json()  # Get JSON data from JavaScript
    name = data.get('name', '')  # Extract 'name' from JSON data
    pin = int(data.get('pin',0))
    state = data.get('state', False)
    status = "ON" if state else "OFF"
    return jsonify(message=f"Hello, {name} {name}! Your gpio number : {pin} {status}")  # Send JSON response

@app.route('/get_temperature', methods=['GET'])
def get_temperature():
    temperature = round(random.uniform(20, 35), 2)  # Simulated data
    return jsonify (message=f"Temperature : {temperature} °C")


@app.route('/get_pir', methods=['GET'])
def get_pir():
    motion_detected = random.choice([True, False])  # Simulated PIR data
    return jsonify(message=f"{motion_detected}" )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

