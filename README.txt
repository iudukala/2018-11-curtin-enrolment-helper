README.txt

Setting up Django backend. Including configuring database. (MySQL)

Please read the entire README.txt/related weblinks BEFORE running any code. 
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


Virtualenv:
Virtualenv is used to isolate a project environment for Python
http://python-guide-pt-br.readthedocs.io/en/latest/dev/virtualenvs/
Please familarise yourself with virtualenvs. 

   When creating a virtualenv use:
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

                                  * * *

MySQL database with Django:
   https://www.digitalocean.com/community/tutorials/how-to-use-mysql-or-mariadb-with-your-django-application-on-ubuntu-14-04

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
   Simply follow the prompts. I used the following credentials and the Django installation currently uses details entered below. 
  
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

  Please everyone see if you can get to the “It Worked!” page with our Django repo. As it is configured to use MySQL, getting to the “It Worked!” page also proves MySQL is setup correctly as well as Django.
