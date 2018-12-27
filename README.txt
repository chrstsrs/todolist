The following steps are needed for deploying the app. The description is also a custom example to the pythonanywhere.com


-----------------------------

Domain name registration

-----------------------------
- 
If we are going to deploy the application properly, we will need a domain name. 
It’s important to have a domain name to serve the application, configure an email 
service and configure an https certificate. Select an accredited registrar (like Namecheap) and register 

your domain. In case you are using pythonanywhere.com this step can be skipped. 


-----------------------------

Transferring the files

-----------------------------


 
- After login to the selected platform transfer the files into the folder you like.
  git clone https://github.com/chrstsrs/todolist.git




-----------------------------

Setting up the virtual environment

-----------------------------

 
- Install (if it is not already there) virtualenvwrapper using pip: 

  pip install virtualenvwrapper



- Next on the same console type:
  
  export WORKON_HOME=~/Envs

  mkdir -p $WORKON_HOME

  source /usr/local/bin/virtualenvwrapper.sh

and now we can create a virtual environment named tdl or whatever you like. 

However, in the next the name tdl will be used for the explanation.:



- Install a virtual environment with python 3.7 and activate it. Since they use Make 

Virtual Environment we create it like: 
  
mkvirtualenv --python=/usr/bin/python3.7 tdl 

tdl is the name of the virtual environment. It will also install in it Python3.7, 

the version we are using for the project. Make Virtual Environment (mkvirtualenv) 
will activate our environment just after the installation.



- Install all the dependencies including Django for our project:
 
 pip install -r todolist/requirements/production.txt



- Install the driver to access the DB you are going to use: 
  For example:

  - for a MySQL db you have to write the command: 
    pip install mysqlclient.


  - If you choose Postgres it is prefered to install the psycopg2 module

    (and declare it in the ENGINE variable as described later on), use the command:
     pip install psycopg2

-----------------------------
Create the web app

-----------------------------

- From the console tab, select add a new app and then manual configuration. Select 

your domain name. However, in the free host 
of pythonanywhere.com, you can not have this choice. 
Select to create a Django app and then make some more configuration.



- Link the path to the virtual environment. That is usual 

    /home/<your_account_name>/Envs/<your_virtual_environment_name> 
  like:

    /home/chrstsrs/Envs/tdl



- Locate from the configuration console the WSGI file and update it. Uncomment 
the section about Django and write the correct path of the application 
(ie path = '/home/chrstsrs/todolist'). Change the name of the 
DJANGO_SETTINGS_MODULE to 'todolist.settings.production' and delete 
the previous code appears before the Django section.



- Since you must be able to work from the console as well, you have to specify
the DJANGO_SETTINGS_MODULE variable. To do that locate the postactivate file of 

your virtual environment. This file must be in the   /home/<your_account_name>/Envs/tdl/bin folder. 
  (ex. /home/chrstsrs/Envs/tdl/bin)
and append at the end of the file:
 
  set -a; export DJANGO_SETTINGS_MODULE="todolist.settings.development"; set +a



- After this configuration deactivate the virtual environment and reactivate it 
again, to apply the changes. You will face errors later if you miss that point. 
Use the commands:
   deactivate

and then

  workon tdl 

to do that.



-----------------------------

Create the database

-----------------------------

- Install the python module for the selected database. Choose the DataBase you want 

and create it. When you create it, copy the password of the database and keep it 
safe as you will need it later on. The suggested modules for the database you are 
going to use are:

  
  - In case of MySQL:
       It is recommended by Django to use the msqclient module. You can do that by:
          pip install mysqlclient
\
  - In case of PostgreSQL:

    Although Django provides the postgresql backend, it is advisable to use the 
        postgresql_psycopg2 backend that is part of the psycopg2 module. The postgresql 
    backend belongs to psycopg and is not supported any more. To install it use the     command:

      pip install psycopg2

-----------------------------
Static Files
-----------------------------
- Copy the static files to the STATIC_ROOT folder. Using the bash console, move to the folder where the manage.py file is. (In pythonanywhere.com it must be in 
/home/chrstsrs/todolist) Use the command:
 
  python manage.py collectstatic

to copy all the static files to the $home/assets folder.



- Associate the STATIC_URL with the STATIC_ROOT directory that came out from the 
previus step. In pythonanywhere.com access the tab Web and desclare the URL and 
the directtory. The URL must be /static/ and the directory must have the form 
/home/<user_host>/todolist/assets/ (ex. /home/chrstsrs/todolist/assets/) 



-----------------------------

Setup an SMTP email service

-----------------------------

- There are many choices like mailgun, sendgrid or Gmail, that can be used for the 
email service. The steps for each server are provided by the host. To do this using 

Google's Gmail, obtain an API password from an existing Gmail and keep it safe. 
it will be needed later on.



-----------------------------

Update the settings module

-----------------------------

- create a .env file and add the environment variables:


  - ALLOWED_HOSTS. Specify the right domain that will be used in ALLOWED_HOSTS 
        like ALLOWED_HOSTS=.localhost or 'chrstsrs.pythonanywhere.com', 
      or the domain you are going to host this app.



  - The database connection variables DB_NAME, USER, PASSWORD, HOST that will be
        used in the settings/production.py file as the fields:
        'NAME'    : 'DB_NAME',
        'USER'    : 'DB_USER',
        'PASSWORD': 'DB_PASSWORD',
        'HOST'    : 'DB_HOST'
    In the file settings/production.py, write also the name of the ENGINE you 
    are going to use in the default databases field. ie:        
    'ENGINE': 'django.db.backends.mysql',
       or
    'ENGINE': 'django.db.backends.postgresql_psycopg2',

    [NOTE: It is advisible to use the above engine than the 
    'ENGINE': 'django.db.backends.postgresql' provided by Django. 
     In this case, you must have already installed it earlier with 
     the pip command, as already mentioned.],
       or
    'ENGINE': 'django.db.backends.sqlite3',

    [If you want to host it on pythonanywhere.com, you have the variable
     'DB_NAME' must be set as '<your_username>$<your_database_name>'. Keep
     the $ sign in the middle without any extra space.]
       
  - The email service you are going to use. The required fields are: 
    EMAIL_BACKEND EMAIL_HOST EMAIL_PORT EMAIL_HOST_USER EMAIL_HOST_PASSWORD
    EMAIL_USE_TLS. The equivailent fields in the settings/production.py file are:
       EMAIL_BACKEND       : 'EMAIL_BACKEND', 
       EMAIL_HOST          : 'EMAIL_HOST', 
       EMAIL_PORT          : 'EMAIL_PORT', 
       EMAIL_HOST_USER     : 'EMAIL_HOST_USER', 
       EMAIL_HOST_PASSWORD : 'EMAIL_HOST_PASSWORD', 
       EMAIL_USE_TLS       : 'EMAIL_USE_TLS'
    In the password field, you do not provide the real password you have for 
    sign in but the generated one for this API. For Gmail use:
    The Gmail host is smtp.gmail.com. The other fields are provided in your 
    email settings.

  As an example a .env file could be:
SECRET_KEY=*zt@!yb*z!q*!#wpca_q-2012m)+*80t2n=x)0i5sf=taoj21z
ALLOWED_HOSTS=chrstsrs.pythonanywhere.com
DB_NAME=chrstsrs$tasklist
DB_USER=chrstsrs
DB_PASSWORD=M8YFP412P0FGdTRQSDet864DCGYAq
DB_HOST=chrstsrs.mysql.pythonanywhere-services.com
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=chrstsrs@gmail.com
EMAIL_HOST_PASSWORD=wcppzgzwflfilgnv
EMAIL_USE_TLS=True

-----------------------------
Forcing HTTPS 

-----------------------------

- Enable the forcing HTTPS. This will redirect automatically any HTTP connection to 

an HTTPS one.  
 




-----------------------------

Migrate

-----------------------------

- Migrate the project with the commands: 
    
    python manage.py makemigrations

    python manage.py migrate



-----------------------------

Reload your page

-----------------------------

- Reload the page and open a new tab to see the results. There are also log files generated in case of an error. 



