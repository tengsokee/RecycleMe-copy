# RecycleMe

###1
Install dependencies for project. MySQL and its associated modules may not be installed. Install from the MySQL site or OS-specific package managers. Use a dependencies manager like pipenv or virtual env to separate modules dependencies for different projects.
pipenv install -r requirements.txt or pip install -r requirements.txt

###2
start mysql server using command prompt and connect using root user. Create database named 'RecycleMe'. Create mysql user with name 'recycleme' and password 'Recycleme@123'

###3
(Django tutorial: https://docs.djangoproject.com/en/3.1/intro/tutorial01/)
Edit code in models.py: this file contains all the classes. After editing the code, go to RecycleMe/mainApp and run python manage.py makemigrations and python manage.py migrate to update changes in models to the database.
Edit code in views.py: this file contains logic for each web page.
Edit code in urls.py: this file contains URL mapping for each view.
Edit code in forms.py: this file contains classes to allow user to POST data to the website.
Create <filename>.html: this file is the HTML webpage for each URL
If necessary, add CSS code to static/style.css for styling of HTML webpage
If necessary, use javascript to create interactive webpage

###4
Run manage.py in RecycleMe/mainApp with command "python manage.py runserver" and go to http://localhost:8000/community/<url in urls.py> for social media webpages and http://localhost:8000/map/<url in urls.py> for the map
Eg:
http://localhost:8000/community/
http://localhost:8000/community/2/

###5
To add data to database, either run scripts to add to database, or run SQL commands at database server, or run django server and go to http://localhost:8000/admin/
For last option, there is a need to create a django admin account (refer to https://docs.djangoproject.com/en/3.1/intro/tutorial02/) and register the models in the respective admin.py file in the same directory.

###6
Use NumPy/SciPy Docstrings for documentation (refer to https://realpython.com/documenting-python-code/)
Use Sphinx for consolidating documentation 
https://medium.com/@richdayandnight/a-simple-tutorial-on-how-to-document-your-python-project-using-sphinx-and-rinohtype-177c22a15b5b
https://www.youtube.com/watch?v=b4iFyrLQQh4


