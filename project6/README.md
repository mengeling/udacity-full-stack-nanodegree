# Linux Server Configuration

## Server Details
* Public IP: 52.14.167.89
* SSH Port: 2200
* URL: http://52.14.167.89/ or http://ec2-52-14-167-89.us-east-2.compute.amazonaws.com

## Software Installed
* Amazon Lightsail Server Instance
* Apache
* WSGI Apache Module
* PostgreSQL
* Git
* Python Modules Listed Below

## Configurations
1. Update all packages on the server
  * `sudo apt-get update`
  * `sudo apt-get upgrade`
2. Change SSH port from 22 to 2200
  * `sudo nano /etc/ssh/sshd_config`
  * Change the line that says `Port 22` to `Port 2200`
  * `sudo service sshd restart`
3. Configure firewall to deny incoming requests and allow outgoing requests by default
  * `sudo ufw default deny incoming`
  * `sudo ufw default allow outgoing`
4. Configure firewall to allow SSH, HTTP, and NTP requests, and then enable the firewall
  * `sudo ufw allow 2200/tcp`
  * `sudo ufw allow www`
  * `sudo ufw allow ntp`
  * `sudo ufw enable`
  * Also add port 2200 and port 123 on the Networking page of the instance console on https://lightsail.aws.amazon.com
5. Create grader user
  * `sudo adduser grader`
  * Create temporary password
  * Use the `sudo nano /etc/ssh/sshd_config` command to change the line that says `PasswordAuthentication no` to `PasswordAuthentication yes`
  * `sudo service sshd restart`
6. Give grader user sudo permission
  * `sudo nano /etc/sudoers.d/grader`
  * Type `grader ALL=(ALL) NOPASSWD:ALL` and then save and exit the file
6. Create SSH key pair for grader
  * Open new local terminal window
  * Generate key pair with `ssh-keygen`
  * Type current directory's path plus **/.ssh/grader-key-pair**
  * Hit enter to leave passphrase empty
  * Type `cat .ssh/grader-key-pair.pub` and copy the contents of the file
7. Place SSH key pair on server
  * Log into the server as the grader
  * `mkdir .ssh`
  * `nano .ssh/authorized_keys`
  * Paste the contents of the local key pair file and save and exit the file
  * Set file permissions with `chmod 700 .ssh` and `chmod 644 .ssh/authorized_keys`
  * Go back to the **sshd_config** file to turn password authentication off
8. Change timezone to UTC
  * `sudo dpkg-reconfigure tzdata`
  * Select **None of the above** for the geographic area and then **UTC**
9. Install Apache and mod_wsgi Module
  * `sudo apt-get install apache2`
  * `sudo apt-get install libapache2-mod-wsgi`
  * `sudo service apache2 restart`
10. Install PostgreSQL
  * `sudo apt-get install postgresql postgresql-contrib`
  * Run `sudo nano /etc/postgresql/9.5/main/pg_hba.conf` to confirm remote connections to PostgreSQL aren't allowed
11. Create a PostgreSQL database and database user named **catalog**
  * Type `sudo -u postgres createuser -P catalog` to create the user with a password
  * Type `sudo -u postgres createdb -O catalog catalog` to create the database with the user as the owner of it
12. Install Git
  * `sudo apt-get install git`
13. Set up movie catalog application in the server
  * Type `sudo mkdir /var/www/catalog && cd $_` to create **catalog** directory in Apache's root directory
  * Clone the project using `sudo git clone https://github.com/mengeling/udacity-full-stack-project-4.git`
  * Type `sudo mv udacity-full-stack-project-4 catalog && cd $_` to rename directory and move into it
14. Make changes to **catalog** files
  * Rename the **app.py** file to init with `sudo mv app.py __init__.py`
  * Run `sudo nano __init__.py` and add the full client secrets file path when the file is opened here:
  ```
  open('/var/www/catalog/catalog/client_secrets.json', 'r').read())['web']['client_id']
  ```
  * Also add the full path to this line at the end of the file:
  ```
  oauth_flow = flow_from_clientsecrets('/var/www/catalog/catalog/client_secrets.json', scope='')
  ```
  * Update the authorized JavaScript origins in the project's credentials section on the Google Developers Console and at the end of the **client_secrets** file as seen here:
  ```
  "javascript_origins":["http://ec2-52-14-167-89.us-east-2.compute.amazonaws.com","http://52.14.167.89"]}}
  ```
  * Add the new SQL database to the line in the **__init__.py** file that creates the engine:
  ```
  engine = create_engine('postgresql://catalog:password@localhost/catalog')
  ```
  * Repeat the last step with the **database_setup.py** and **database_movies.py** files
15. Download Python packages
  * `sudo apt-get install python-sqlalchemy`
  * `sudo apt-get install python-psycopg2`
  * `sudo apt-get install python-pip`
  * `sudo pip install flask`
  * `sudo pip install oauth2client`
  * `sudo pip install requests`
16. Set up the database with default movies
  * `sudo python database_setup.py`
  * `sudo python database_movies.py`
17. Configure Apache2
  * Type `sudo nano /etc/apache2/sites-available/catalog.conf` and then add the following script and save the file:
  ```
  <VirtualHost *:80>
         ServerName 52.14.167.89
         ServerAlias ec2-52-14-167-89.us-east-2.compute.amazonaws.com
         ServerAdmin admin@52.14.167.89
	       WSGIScriptAlias / /var/www/catalog/catalog.wsgi
	       <Directory /var/www/catalog/catalog/>
		        Order allow,deny
		        Allow from all
	       </Directory>
	       Alias /static /var/www/catalog/catalog/static
	       <Directory /var/www/catalog/catalog/static/>
		        Order allow,deny
		        Allow from all
	        </Directory>
          ErrorLog ${APACHE_LOG_DIR}/error.log
          LogLevel warn
	        CustomLog ${APACHE_LOG_DIR}/access.log combined
  </VirtualHost>
  ```
  * Enable the virtual host with `sudo a2ensite catalog`
18. Create the .wsgi file referenced in the .conf file
  * Type `sudo nano catalog.wsgi` and then add the following script:
  ```
  #!/usr/bin/python
  import sys
  import logging
  logging.basicConfig(stream=sys.stderr)
  sys.path.insert(0,"/var/www/catalog/")

  from catalog import app as application
  application.secret_key = 'Add your secret key'
  ```
19. Restart Apache
  * `sudo service apache2 restart`

## References
* https://www.liquidweb.com/kb/changing-the-ssh-port/
* http://www.wikihow.com/Change-the-Timezone-in-Linux
* https://www.digitalocean.com/community/tutorials/how-to-secure-postgresql-on-an-ubuntu-vps
* https://help.ubuntu.com/community/PostgreSQL
* https://help.ubuntu.com/lts/serverguide/httpd.html
* https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps
