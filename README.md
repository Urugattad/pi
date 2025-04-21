connection for ssh

ssh-keygen -R <your ip>
sudo apt install python3-pip

pip install mysql-connector-python --break-system-packages

pip install flask-mail --break-system-packages

pip install flask-mysql-connector --break-system-packages

sudo apt install mariadb-server -y

sudo systemctl status mariadb

sudo systemctl start mariadb

sudo mysql_secure_installation

Press Enter for the current root password (MariaDB uses Unix authentication by default).
Set a new root password when prompted.
Answer Y (Yes) to all security questions.

sudo mysql -u root -p

CREATE DATABASE picloudcontrol;

USE picloudcontrol;

CREATE TABLE gpio_pin_states (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pin INT UNIQUE NOT NULL,
    state BOOLEAN NOT NULL,
    name VARCHAR(50) NOT NULL DEFAULT 'Unknown'
);


CREATE USER 'picloud'@'localhost' IDENTIFIED BY 'toor';
GRANT ALL PRIVILEGES ON picloudcontrol.* TO 'picloud'@'localhost';
FLUSH PRIVILEGES;
EXIT;

//in config.txt

dtoverlay=dht11,gpiopin=26



sudo crontab -e
@reboot file location





python3 app.py --host=0.0.0.0

