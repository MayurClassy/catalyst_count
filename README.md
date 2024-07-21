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

git clone https://github.com/MayurClassy/catalyst_count.git

<img width="348" alt="gitclone" src="https://github.com/user-attachments/assets/70c8e03c-94ce-4090-9489-c614461d73c4">


2.Create a virtual Environment

python -m venv env
source env/bin/activate 

<img width="152" alt="activate" src="https://github.com/user-attachments/assets/2aad72a2-85ad-47f5-8124-dfb7be702ef4">


3.Install Dependencies

pip install -r requirements.txt

<img width="216" alt="requi" src="https://github.com/user-attachments/assets/9d3960af-c358-48ea-b61f-e45adbba50e9">


4.Setup Postgresql
Create a PostgreSQL database and user and Update your .env file with the following:
.env file :

<img width="282" alt="env" src="https://github.com/user-attachments/assets/8a0d1b38-4b7f-4dcb-ad70-f8ab4cb96d0d">


5.Apply migrations

python manage.py makemigrations

<img width="211" alt="makemigrations" src="https://github.com/user-attachments/assets/a0ef8081-b78b-4909-a2ba-c76b6bd978dc">


python manage.py migrate

<img width="171" alt="migrattt" src="https://github.com/user-attachments/assets/ad6b1ea6-4203-40d4-8a7a-781bf8de93bc">


6.Create Superuser

python manage.py createsuperuser

<img width="218" alt="superuser" src="https://github.com/user-attachments/assets/50a64076-75b6-4a3f-bcd7-4b1cf0e30cbd">


7.Run the Development Server

python manage.py runserver

<img width="192" alt="runserver" src="https://github.com/user-attachments/assets/a230f04a-37f3-4a05-9bfb-a0cd88e2243a">

