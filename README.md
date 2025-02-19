sudo apt update && sudo apt upgrade -y
sudo apt install apache2 libapache2-mod-wsgi-py3 python3-pip -y

cd /path/to/your/project
pip install flask

pip install flask-wtf flask-sqlalchemy

nano wsgi.py

from allah import app

if __name__ == "__main__":
    app.run()

sudo nano /etc/apache2/sites-available/picloudcontrol.conf

<VirtualHost *:80>
    ServerName your_raspberrypi_ip

    WSGIDaemonProcess picloudcontrol user=pi group=pi threads=5
    WSGIScriptAlias / /var/www/picloudcontrol/wsgi.py

    <Directory /var/www/picloudcontrol>
        Require all granted
    </Directory>

    Alias /static /var/www/picloudcontrol/static
    <Directory /var/www/picloudcontrol/static/>
        Require all granted
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/picloudcontrol_error.log
    CustomLog ${APACHE_LOG_DIR}/picloudcontrol_access.log combined
</VirtualHost>

sudo mkdir -p /var/www/picloudcontrol
sudo cp -r /path/to/your/project/* /var/www/picloudcontrol/

sudo chown -R www-data:www-data /var/www/picloudcontrol
sudo chmod -R 755 /var/www/picloudcontrol

sudo a2ensite picloudcontrol.conf
sudo systemctl restart apache2

http://your_raspberrypi_ip

sudo systemctl enable apache2

sudo apt update
sudo apt install mysql-server -y
pip install mysql-connector-python flask

sudo mysql_secure_installation

sudo mysql -u root -p

CREATE DATABASE picloud;
USE picloud;

CREATE TABLE gpio_states (
    pin INT PRIMARY KEY,
    state BOOLEAN NOT NULL
);

CREATE USER 'pi'@'localhost' IDENTIFIED BY 'yourpassword';
GRANT ALL PRIVILEGES ON picloud.* TO 'pi'@'localhost';
FLUSH PRIVILEGES;
EXIT;

import mysql.connector
from flask import Flask, request, jsonify, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

USERNAME = 'picloudcontrol'
PASSWORD = 'root'

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="pi",
        password="yourpassword",
        database="picloud"
    )

# Initialize the database (optional, but useful for first-time setup)
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS gpio_states (
        pin INT PRIMARY KEY, 
        state BOOLEAN NOT NULL
    )''')
    conn.commit()
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

    cursor.execute("INSERT INTO gpio_states (pin, state) VALUES (%s, %s) ON DUPLICATE KEY UPDATE state=%s", 
                   (pin, state, state))
    conn.commit()
    conn.close()

    status = "ON" if state else "OFF"
    return jsonify(message=f"GPIO {pin} is now {status}")

@app.route('/get_gpio_states', methods=['GET'])
def get_gpio_states():
    if not session.get('logged_in'):
        return jsonify({'message': 'Unauthorized'}), 401

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM gpio_states")
    gpio_states = cursor.fetchall()
    conn.close()

    return jsonify({row["pin"]: row["state"] for row in gpio_states})

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

