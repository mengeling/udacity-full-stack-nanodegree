# Movie Catalog
This project uses a SQLite database and local server to create a web application for cataloging movies. The application uses third party authentication and authorization with Google, so users can log into the application to add, edit, and delete movies from the database.

## How to Use the Application
1. Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads) and [Vagrant](https://www.vagrantup.com/downloads.html)
2. Download and unzip this file to access the database: [FSND-Virtual-Machine.zip](https://d17h27t6h515a5.cloudfront.net/topher/2017/August/59822701_fsnd-virtual-machine/fsnd-virtual-machine.zip)
3. Fork and clone this GitHub repository to your local machine
4. Move all of the files from the cloned repository into the following directory in your **Downloads** folder: **FSND-Virtual-Machine/vagrant/catalog**
5. Open your terminal and navigate to the **vagrant** directory within the **FSND-Virtual-Machine** directory
6. Type `vagrant up` to set up the virtual machine
7. Once it's done installing, type `vagrant ssh` to log into the virtual machine
8. Type `cd /vagrant/catalog` to navigate to the virtual machine's **catalog** directory that is shared with the **catalog** directory on your local machine
9. Type `ls` to confirm all of the files are in the virtual machine's **catalog** directory
10. Type `python database_setup.py` to set up the SQLite database
11. Type `python database_movies.py` to load the genres and movies into the database
12. Type `python app.py` to run the application
13. Open a browser and go to http://localhost:5000 to use the application

&nbsp;
&nbsp;

![Website Screenshot](/project4/static/screenshot.png?raw=true)
