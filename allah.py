from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Configure SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gpio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

PIR_PIN = 4  # Define the GPIO pin connected to the PIR sensor

# Set up the GPIO pin
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin numbering
GPIO.setup(PIR_PIN, GPIO.IN)

# Hardcoded credentials
USERNAME = "picloudcontrol"
PASSWORD = "root"

# Database Model for GPIO States
class GPIOState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pin = db.Column(db.Integer, unique=True, nullable=False)
    state = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<GPIO {self.pin} - {'ON' if self.state else 'OFF'}>"

# Create the database if it doesn't exist
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))  
    return render_template('std.html')  

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == USERNAME and password == PASSWORD:
            session['user'] = username  
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid credentials!")
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/toggle_gpio', methods=['POST'])
def toggle_gpio():
    if 'user' not in session:
        return jsonify({"error": "Unauthorized"}), 403  

    data = request.get_json()
    pin = int(data.get('pin', 0))
    state = data.get('state', False)

    gpio_entry = GPIOState.query.filter_by(pin=pin).first()
    
    if gpio_entry:
        gpio_entry.state = state  # Update existing pin state
    else:
        gpio_entry = GPIOState(pin=pin, state=state)
        db.session.add(gpio_entry)

    db.session.commit()  # Save to database

    status = "ON" if state else "OFF"
    return jsonify(message=f"GPIO {pin} is now {status}")

@app.route('/get_gpio_states', methods=['GET'])
def get_gpio_states():
    if 'user' not in session:
        return jsonify({"error": "Unauthorized"}), 403  

    gpio_entries = GPIOState.query.all()
    gpio_states = {entry.pin: entry.state for entry in gpio_entries}
    return jsonify(gpio_states)

@app.route('/get_temperature', methods=['GET'])
def get_temperature():
    if 'user' not in session:
        return jsonify({"error": "Unauthorized"}), 403  

    temperature = round(random.uniform(20, 35), 2)
    return jsonify(message=f"{temperature}")

@app.route('/get_pir', methods=['GET'])
def get_pir():
    if 'user' not in session:
        return jsonify({"error": "Unauthorized"}), 403  

    motion_detected = GPIO.input(PIR_PIN)  # Read actual PIR sensor state
    motion_status = "Detected" if motion_detected else "Undetected"  # Custom output

    return jsonify(message=motion_status)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
