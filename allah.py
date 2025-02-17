from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
import RPi.GPIO as GPIO
import random

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Enable WebSocket

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Dictionary to track GPIO states
gpio_states = {}

@app.route('/')
def index():
    return render_template('std.html')

@socketio.on('toggle_gpio')
def handle_gpio_toggle(data):
    pin = int(data.get('pin', 0))
    state = data.get('state', False)

    if pin not in gpio_states:
        GPIO.setup(pin, GPIO.OUT)  

    GPIO.output(pin, state)
    gpio_states[pin] = state  # Store state persistently

    # Broadcast the updated state to all clients
    emit('update_gpio', {'pin': pin, 'state': state}, broadcast=True)

@socketio.on('request_gpio_states')
def send_gpio_states():
    emit('update_all_gpio', gpio_states)

@app.route('/get_temperature', methods=['GET'])
def get_temperature():
    temperature = round(random.uniform(20, 35), 2)  # Simulated sensor data
    return jsonify(message=f"{temperature}")

@app.route('/get_pir', methods=['GET'])
def get_pir():
    motion_detected = random.choice([True, False])  # Simulated PIR data
    return jsonify(message=f"{motion_detected}")

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", debug=True)
