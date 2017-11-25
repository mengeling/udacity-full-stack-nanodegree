# Logs Analysis
For this project, I created an internal reporting tool that determines which news articles and authors are generating the most interest. The tool also flags days on which more than 1% of online requests lead to errors. The Python program uses the `psycopg2` module to run complex SQL queries on the news site's internal database, and then the results are returned to the user in plain text.

## How to Use the Tool
1. Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads), [Vagrant](https://www.vagrantup.com/downloads.html), and [psycopg2](http://initd.org/psycopg/download/)
2. Download and unzip this file to access the database: [FSND-Virtual-Machine.zip](https://d17h27t6h515a5.cloudfront.net/topher/2017/August/59822701_fsnd-virtual-machine/fsnd-virtual-machine.zip)
3. Download and unzip the [newsdata.sql](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) file and save it in the **vagrant** sub-directory of the **FSND-Virtual-Machine** directory in your **Downloads**
4. Fork and clone this GitHub repository to your local machine
5. Copy the **news_analysis.py** file from the cloned repository into the same  **vagrant** directory as above
6. Open your terminal and navigate to the **vagrant** directory within the **FSND-Virtual-Machine** directory
7. Type `vagrant up` to set up the virtual machine
8. Once it's done installing, type `vagrant ssh` to log into the virtual machine
9. Type `cd /vagrant` to navigate to the directory that is shared with the **vagrant** directory on your computer
10. Confirm the **newsdata.sql** and **news_analysis.py** files are in the virtual machine's **vagrant** directory
11. Type `python news_analysis.py` to run the program
