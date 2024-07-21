Catalyst Count
Catalyst Count is a web application built with Django 3.x/4.x, PostgreSQL, and Bootstrap 4/5. The application allows users to log in and upload large CSV files (up to 1GB) with a visual progress indicator. Once the file is uploaded, the database is updated with the contents of the file. Users can then filter the data using a query builder form and view the count of records based on applied filters.

Requirements
Python 3.x
Django 3.x/4.x
PostgreSQL
Git
Virtualenv

Installation:

1.Clone the repository:
git clone https://github.com/MayurClassy/catalyst-count.git

2.Create a virtual Environment
python -m venv env
source env/bin/activate 

3.Install Dependencies
pip install -r requirements.txt

4.Setup Postgresql
Create a PostgreSQL database and user and Update your .env file with the following:
.env file :
<img width="282" alt="env" src="https://github.com/user-attachments/assets/8a0d1b38-4b7f-4dcb-ad70-f8ab4cb96d0d">


5.Apply migrations
python manage.py makemigrations
python manage.py migrate

6.Create Superuser
python manage.py createsuperuser

7.Run the Development Server
python manage.py runserver
