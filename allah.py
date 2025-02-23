from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import RPi.GPIO as GPIO
import mysql.connector
import time
import os
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for session management

# Email Configuration
SMTP_SERVER = "smtp.gmail.com"  
SMTP_PORT = 587  # TLS Port
EMAIL_SENDER = "gurudatta220928@gmail.com"
EMAIL_PASSWORD = "lapg qrkm pdvd hthg" 
EMAIL_RECEIVER = "gpaykaru@gmail.com"

# User credentials
USERNAME = 'pi'
PASSWORD = 'root'

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="picloud",
    password="toor",
    database="picloudcontrol"
)
cursor = db.cursor()

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Function to read temperature sensor (if available)
DEVICE_PATH = "/sys/bus/iio/devices/iio:device0"
def read_first_line(filename):
    try:
        with open(filename, "rt") as f:
            return True, int(f.readline())
    except (ValueError, OSError):
        return False, 0  # Return 0 if reading fails
def send_email_alert():
    msg = EmailMessage()
    msg["Subject"] = "Motion Detected Alert!"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg.set_content("Warning: Motion detected on your Raspberry Pi!")

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Secure the connection
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(" Email sent successfully!")
    except Exception as e:
        print(f" Failed to send email: {e}")
        
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
    return render_template('std.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

# Toggle GPIO and store in MySQL
@app.route('/toggle_gpio', methods=['POST'])
def toggle_gpio():
    if not session.get('logged_in'):
        return jsonify({'message': 'Unauthorized'}), 401

    data = request.get_json()
    name = data.get('name', '')
    pin = int(data.get('pin', 0))
    state = data.get('state', False)

    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, state)

    cursor.execute("INSERT INTO gpio_pin_states (pin, state,name) VALUES (%s, %s,%s) ON DUPLICATE KEY UPDATE state=%s",
                   (pin, state,name, state))
    db.commit()

    return jsonify(message=f"GPIO {pin} is now {'ON' if state else 'OFF'}")

@app.route('/save_gpio', methods=['POST'])
def save_gpio():
    if not session.get('logged_in'):
        return jsonify({'message': 'Unauthorized'}), 401
    data = request.get_json()
    name = data.get('name', '')
    pin = int(data.get('pin', 0))
    state = data.get('state', False)
    
    # Store in MySQL
    cursor.execute("INSERT INTO gpio_pin_states (pin, state,name) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE state=%s",
                   (pin, state, name, state))
    db.commit()

    
    return jsonify(message=f"GPIO {pin} is now save")
    

# Get GPIO states from MySQL
@app.route('/get_gpio_states', methods=['GET'])
def get_gpio_states():
    if not session.get('logged_in'):
        return jsonify({'message': 'Unauthorized'}), 401

    cursor.execute("SELECT pin, state, name FROM gpio_pin_states")
    gpio_data = [{"pin": row[0], "state": bool(row[1]), "name": row[2]} for row in cursor.fetchall()]

    return jsonify(gpio_data)

# Delete GPIO entry and turn it off
@app.route('/delete_gpio', methods=['POST'])
def delete_gpio():
    if not session.get('logged_in'):
        return jsonify({'message': 'Unauthorized'}), 401

    data = request.get_json()
    pin = int(data.get('pin', 0))

    # Turn off GPIO before deleting
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)

    # Delete from MySQL
    cursor.execute("DELETE FROM gpio_pin_states WHERE pin = %s", (pin,))
    db.commit()

    return jsonify(message=f"GPIO {pin} deleted successfully")

# Get temperature sensor data
@app.route('/get_temperature', methods=['GET'])
def get_temperature():
    if not session.get('logged_in'):
        return jsonify({'message': 'Unauthorized'}), 401

    flag, temperature = read_first_line(DEVICE_PATH + "/in_temp_input")
    temperature_value = (temperature // 1000) if flag else "N.A."

  
  
    return jsonify(message=f"{temperature_value}")

# Get PIR motion sensor data
@app.route('/get_pir', methods=['GET'])
def get_pir():
     if not session.get('logged_in'):
        return jsonify({'message': 'Unauthorized'}), 401

    motion_detected = True

    if motion_detected:
        print(" Motion detected!")
        send_email_alert()

    return jsonify(motion=bool(motion_detected))

   

if __name__ == '__main__':
    try:
        app.run(host="0.0.0.0", debug=True)
    finally:
        GPIO.cleanup()  # Ensure GPIO is properly reset
        db.close()  # Close MySQL connection
