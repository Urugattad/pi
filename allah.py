from flask import Flask, request, jsonify, render_template
import RPi.GPIO as GPIO
import random

app = Flask(__name__)

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Dictionary to track GPIO states
gpio_states = {}

@app.route('/')
def index():
    return render_template('std.html')  # Load the HTML page

@app.route('/toggle_gpio', methods=['POST'])
def toggle_gpio():
    data = request.get_json()
    pin = int(data.get('pin', 0))
    state = data.get('state', False)

    if pin not in gpio_states:
        GPIO.setup(pin, GPIO.OUT)  # Set pin as output

    GPIO.output(pin, state)
    gpio_states[pin] = state  # Store pin state

    status = "ON" if state else "OFF"
    return jsonify(message=f"GPIO {pin} is now {status}")

@app.route('/get_gpio_states', methods=['GET'])
def get_gpio_states():
    return jsonify(gpio_states)

@app.route('/get_temperature', methods=['GET'])
def get_temperature():
    temperature = round(random.uniform(20, 35), 2)  # Simulated data
    return jsonify(message=f"{temperature}")

@app.route('/get_pir', methods=['GET'])
def get_pir():
    motion_detected = random.choice([True, False])  # Simulated PIR data
    return jsonify(message=f"{motion_detected}")

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)


demo


from flask import Flask, request, jsonify, render_template
import random

app = Flask(__name__)

# Dictionary to track GPIO states
gpio_states = {}

@app.route('/')
def index():
    return render_template('std.html')  # Load the HTML page

@app.route('/toggle_gpio', methods=['POST'])
def toggle_gpio():
    data = request.get_json()
    pin = int(data.get('pin', 0))
    state = data.get('state', False)

    gpio_states[pin] = state  # Store pin state

    status = "ON" if state else "OFF"
    return jsonify(message=f"GPIO {pin} is now {status}")

@app.route('/get_gpio_states', methods=['GET'])
def get_gpio_states():
    return jsonify(gpio_states)

@app.route('/get_temperature', methods=['GET'])
def get_temperature():
    temperature = round(random.uniform(20, 35), 2)  # Simulated data
    return jsonify(message=f"{temperature}")

@app.route('/get_pir', methods=['GET'])
def get_pir():
    motion_detected = random.choice([True, False])  # Simulated PIR data
    return jsonify(message=f"{motion_detected}")

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
