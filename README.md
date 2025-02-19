sudo apt update
sudo apt install postgresql postgresql-contrib -y
pip install psycopg2 flask

sudo systemctl start postgresql
sudo systemctl enable postgresql

sudo -i -u postgres
psql

CREATE DATABASE picloud;
CREATE USER pi WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE picloud TO pi;

\c picloud

CREATE TABLE gpio_states (
    pin INT PRIMARY KEY,
    state BOOLEAN NOT NULL
);

\q
exit



import psycopg2
from flask import Flask, request, jsonify, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

USERNAME = 'picloudcontrol'
PASSWORD = 'root'

# Database connection function
def get_db_connection():
    return psycopg2.connect(
        dbname="picloud",
        user="pi",
        password="yourpassword",
        host="localhost"
    )

# Initialize the database (ensures the table exists)
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS gpio_states (
        pin INT PRIMARY KEY, 
        state BOOLEAN NOT NULL
    )''')
    conn.commit()
    cursor.close()
    conn.close()

init_db()  # Ensure the table exists

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

@app.route('/toggle_gpio', methods=['POST'])
def toggle_gpio():
    if not session.get('logged_in'):
        return jsonify({'message': 'Unauthorized'}), 401

    data = request.get_json()
    pin = int(data.get('pin', 0))
    state = bool(data.get('state', False))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO gpio_states (pin, state) 
        VALUES (%s, %s) 
        ON CONFLICT (pin) DO UPDATE SET state = EXCLUDED.state
    """, (pin, state))

    conn.commit()
    cursor.close()
    conn.close()

    status = "ON" if state else "OFF"
    return jsonify(message=f"GPIO {pin} is now {status}")

@app.route('/get_gpio_states', methods=['GET'])
def get_gpio_states():
    if not session.get('logged_in'):
        return jsonify({'message': 'Unauthorized'}), 401

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM gpio_states")
    gpio_states = cursor.fetchall()
    conn.close()

    return jsonify({pin: state for pin, state in gpio_states})

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)




document.addEventListener("DOMContentLoaded", function () {
    fetch('/get_gpio_states')
        .then(response => response.json())
        .then(data => {
            for (const [pin, state] of Object.entries(data)) {
                let switchElement = document.querySelector(`#toggle-${pin}`);
                if (switchElement) {
                    switchElement.checked = state == 1;  // Restore toggle state
                }
            }
        })
        .catch(error => console.error('Error fetching GPIO states:', error));
});


sudo systemctl restart apache2


python3 -c "import Adafruit_DHT; print('Adafruit_DHT installed successfully!')"



sudo crontab -e
@reboot file location





python3 app.py --host=0.0.0.0

