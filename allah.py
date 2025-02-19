from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import random
import RPi.GPIO as GPIO

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for session management

# User credentials
USERNAME = 'picloudcontrol'
PASSWORD = 'root'

# Dictionary to track GPIO states
gpio_states = {}

gpio_pir = 4  # PIR sensor pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_pir, GPIO.IN)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/home')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('std.html')  # Load the HTML page

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/toggle_gpio', methods=['POST'])
def toggle_gpio():
    if not session.get('logged_in'):
        return jsonify({'message': 'Unauthorized'}), 401
    data = request.get_json()
    pin = int(data.get('pin', 0))
    state = data.get('state', False)

    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, state)
    gpio_states[pin] = state

    status = "ON" if state else "OFF"
    return jsonify(message=f"GPIO {pin} is now {status}")

@app.route('/get_temperature', methods=['GET'])
def get_temperature():
    if not session.get('logged_in'):
        return jsonify({'message': 'Unauthorized'}), 401
    temperature = round(random.uniform(20, 35), 2)  # Simulated data
    return jsonify(message=f"{temperature}")

@app.route('/get_pir', methods=['GET'])
def get_pir():
    if not session.get('logged_in'):
        return jsonify({'message': 'Unauthorized'}), 401
    motion_detected = GPIO.input(gpio_pir)
    return jsonify(message="Motion Detected" if motion_detected else "Motion Not Detected")

if __name__ == '__main__':
    try:
        app.run(host="0.0.0.0", debug=True)
    finally:
        GPIO.cleanup()
