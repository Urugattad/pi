# pi
sudo nano /etc/systemd/system/flask_gpio.service


ls /etc/systemd/system/

sudo crontab -e

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
