from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import RPi.GPIO as GPIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Enable real-time WebSockets

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Dictionary to store GPIO states
gpio_states = {}

@app.route('/')
def index():
    return render_template('std.html')  # Load the frontend page

@socketio.on('connect')
def handle_connect():
    """Send the current GPIO states to the newly connected client."""
    emit('update_all_gpio', gpio_states)

@socketio.on('toggle_gpio')
def handle_gpio_toggle(data):
    """Toggle GPIO state and broadcast the change."""
    pin = int(data['pin'])
    state = data['state']

    if pin not in gpio_states:
        GPIO.setup(pin, GPIO.OUT)  # Setup pin only if not already done

    GPIO.output(pin, state)
    gpio_states[pin] = state  # Store the new state

    # Broadcast the new state to all connected clients
    emit('update_gpio', {'pin': pin, 'state': state}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", debug=True)
