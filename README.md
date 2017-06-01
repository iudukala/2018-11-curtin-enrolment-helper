# Enrolment Helper
    Group: 11.3
    * Yoakim Persson
    * Campbell Pedersen
    * Chen Bi
    * Thien Quang Trinh
    * Chung-Yen Lu

### Overview
    Project is a Django powered website designed to help own client, Hannes Herrmann, create student enrolment plans.
    MySQL provides the nessassary database. Outlined below are all the step required to setup the project. 
    This setup was created on a Linux machine, however it should be completely compatible with Mac computers. Microsoft 
    computers my required some alteratives however for components such as the MySQL setup, the process should be the same.

### System/files layout. 
    This may change depending on how tests are setup and is only going to be required if you wish to run tests on
    your local machine.

    Tests can be currently run as:
    'python manage.py test core_app'

    It is highly recommended to read all of the document and linked sites prior to running all code. Please read the 
    entire README.txt/related weblinks BEFORE running any code. 
    Also always check that you are using the virtualenv when running commands, and deactive when you are done.

    Once setup use the 
    $ python manage.py runserver
    In initilise a locally hosted Django 

       Please create a project folder to hold all Project related material.
       My current directory layout:
       (Just to give an idea on what my project layout looks like.)

       SEP2_Project
          |—  project_env
          |      |- bin/activate
          |      |- /lib/
          |      |- ...
          |
          |—  Enrolment_Helper (REPOSITORY)
                 |- requirements.txt
                 |- manage.py
                 |—  Enrolment_Helper/
                          |- __init__.py
                          |- urls.py
                          |- wsgi.py
                          |- settings.py
                          |- __pycache__/

                                  * * *


### Setting up the virtual environment:
    Virtualenv is used to isolate a project environment for Python.
    http://python-guide-pt-br.readthedocs.io/en/latest/dev/virtualenvs/
    Please familiarise yourself with virtualenvs. 

    When creating a virtualenv:
    We all need to be using the same versions on varies software.
    We will be using Python3.5
    To determine where python3.5 is on your system:
    $ type python3.5
    $ virtualenv -p /usr/bin/python3.5 project_env
    $ source ./project_env/bin/activate
    To test that virtualenv is working run
    $ type python
    Should display that python is being run from within the virtualenv.
    To disconnect from the virtualenv run
    $ deactivate


    Clone Git from our BitBucket project next to the project_env folder. 
    Make sure you are using the virtualenv still.
    Navigate to the project root folder.
    Run 
    $ pip install -r requirements.txt 
    This will install the same versions for all of us (Currently really only Django and MySQL stuff)

    If you wish to try out the Django installation WITHOUT MySQL simply to try and run it open
    Enrolment_Helper/Settings.txt and in the database section comment the MySQL stuff and uncomment the SQLite stuff.

    $ python manage.py runserver 

### MySQL database with Django:

    The following website provides an detailed method for setting up and linking a MySQL database with Django. 
    https://www.digitalocean.com/community/tutorials/how-to-use-mysql-or-mariadb-with-your-django-application-on-ubuntu-14-04
    
    Please follow along with the tutorial and use the values listed below when nessassary.

    Tutorial did not work directly for me due to my current version of MySQL being newer then tutorial.
    I Already had MySQL installed and had forgotten password, therefore run to remove mysql completely

    (Use with caution)
    $ sudo apt purge mysql*

    (The following the ‘digitalocean’ installation process for MySQL)
    $ sudo apt
    $ sudo apt install python-pip python-dev mysql-server libmysqlclient-dev

    NOTE: Newer versions of MySQL does not require the,
    ‘sudo mysql_install_db’ command.
    Run
    $ mysql_secure_installation
    Simply follow the prompts. I used the following credentials and the Django installation currently uses details 
    entered below. 

    Mysql_Server-5.7
    User: root 
    Passwd: root 

    Database: Enrolment_Helper
    User: enrolment_helperuser
    Passwd: user

    $ python manage.py makemigrations
    $ python manage.py migrate

    $ python manage.py createsuperusr

    Django_Superuser:
    Username: yoakim
    Email: 17080170@student.curtin.edu.au
    Passwd: yoakim_django

    Once you have reached the “It Worked!” you can append /admin to the URL and use the django superuser details
    to login to the admin page.

    Please everyone see if you can get to the “It Worked!” page with our Django repo. As it is configured to use MySQL, 
    getting to the “It Worked!” page also proves MySQL is setup correctly as well as Django.
 
## Testing
    For testing purposes, the tests are conducted on a new database created from the current models.
    This is obviously good as it isolates the existing databases from test data.
    The test data (which is created and destroyed for the test) is called 'test_Enrolment_Helper' (in own case).
    However the user (enrolment_helperuser) does not have permission to do anything with with database.

    To fix:
    Login to mySQL as root.
    'GRANT ALL PRIVILGES ON test_Enrolment_Helper.* TO enrolment_helperuser@localhost;'
    'FLUSH PRIVILEGES;'
    
    Tests for the system can how be run with:
    'python manage.py test core_app.tests

### Virtual Machine
    We have provided a virtual machine running Linux Mint with the project configured.
    VM login:
    Username: Hannes
    Password: herrmann
    
    root user:
    Password: hannes
    
    A folder containing the project exists in the home directory. 'ENROLMENT_HELPER'
    This folder contains several project related folders and documents including the enrolment PDF files which were 
    used extensively throughout the project.
    The project itself is within the '2017-11.3-enrolment_helper' folder.
    From within this folder it is possibly to launch the server, which them can be opened in the web browser located 
    on the VM, as well as run tests.
    
    It is required to perform all Django server tasks within the Virtualenv.
    To activate:
    'source virtualenv/bin/activate'
    
    To deactivate:
    'deactivate'
    
    Running the server:
    'python manage runserver'
   
    # BACKUP
    Database backup are currently created periodically with 'Cron' everyday at 4:00am.
    Manual backups are possible using the command:
    'python manage.py runcrons' OR 'python manage.py dbbackup'
    
    To restore a backup
    'python manage.py dbrestore -i <DATABASEFILE_NAME> -I <DATABASEFILE_PATH>'
    
    Backup documentation:
    Please refer back to the documentation if you wish to use a different settings.
    http://django-dbbackup.readthedocs.io/en/stable/
    For cron settings/setup.
    http://django-cron.readthedocs.io/en/latest/
    
    # Encryption/Decryption  
    Encryption and decryption is provided via Django fernet fields.
    
    Encryption occurs at the database and backup created with the above tools with also contain encrypted values.
    The encryption key is the django 'secret key' so please do not change/generate a new key without consultanting the 
    documentation below.
    
    Documention
    https://django-fernet-fields.readthedocs.io/en/latest/
