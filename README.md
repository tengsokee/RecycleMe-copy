# RecycleMe

###1
Install dependencies for project. 
change to source directory, and run pipenv install -r requirements.txt or pip install -r requirements.txt
P.S. MySQL and its associated modules may not be installed. Install from the MySQL site or OS-specific package managers. Use a dependencies manager like pipenv or virtual env to separate modules dependencies for different projects.

###2
start mysql server using command prompt and connect using root user. Create database named 'RecycleMe'. Create mysql user with name 'recycleme' and password 'Recycleme@123'

###3
Assuming you are at root directory, run 
mysql -u username -p -h localhost recycleme<recycleme.sql to import the database data. 
P.S. replace username with your MySQL username.

###4
Run manage.py in RecycleMe/mainApp with command "python manage.py runserver" and go to http://localhost:8000/community/<url in urls.py> for social media webpages and http://localhost:8000/map/<url in urls.py> for the map
Eg:
http://localhost:8000/community/
http://localhost:8000/community/

