python
import guizero
pip3 install guizero --break-system-packages

python3 -c "import Adafruit_DHT; print('Adafruit_DHT installed successfully!')"

sudo apt install python3-pip python3-dev build-essential -y

sudo apt update && sudo apt upgrade -y

pip install flask flask-sqlalchemy

python3 --version
pip3 --version


sudo apt install python3 python3-pip -y


pip3 install flask-socketio eventlet gevent

pip3 install gevent gevent-websocket

# pi
sudo nano /etc/systemd/system/flask_gpio.service


ls /etc/systemd/system/

sudo crontab -e
@reboot file location

[Unit]
Description=Flask GPIO Control Web App
After=multi-user.target

[Service]
User=pi
ExecStart=/usr/bin/python3 /home/pi/flask_gpio_app/app.py --host=0.0.0.0
WorkingDirectory=/home/pi/flask_gpio_app
Restart=always

[Install]
WantedBy=multi-user.target



sudo systemctl daemon-reload
sudo systemctl enable flask_gpio
sudo systemctl start flask_gpio



sudo systemctl status flask_gpio




python3 app.py --host=0.0.0.0

method 2 for host

wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-stable-linux-arm.zip
unzip ngrok-stable-linux-arm.zip
sudo mv ngrok /usr/local/bin


ngrok http 5000


https://random-name.ngrok.io
