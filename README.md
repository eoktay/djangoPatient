### Built With

The following are the list of any major frameworks/libraries used to bootstrap this project. 
* [Python](https://python.org/)
* [Django](https://www.djangoproject.com/)


### Prerequisites


All the steps below are done on Ubuntu Desktop as of today's date(09.22.22), with version 22.04.1.
It is highly recommended that this version of Linux be used. Alternatively, apply same steps with 
corresponding commands in their respective environments. 

### Installation


#### Back End Steps
1. Download code, go to its root directory. Install latest version of Python. Install pip: ```sudo apt-get install pip ```
5. Create a virtual environment for this specific project and activate the virtual environment if not exist. Create a database for the project.                                                        
```sudo apt update```
```sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib```  
```sudo -u postgres ```  
*** Commands within the Database connection start ***
```psql ```
```alter user postgres password 'reti';```
```CREATE DATABASE retispec; ```  
```\q ```   
```exit ```       
*** Commands within the Database connection end ***

```python3 -m venv retispec```                                               
```source retispec/bin/activate ``` 
```sudo apt install make ```
```make -version```
6. Install required packages.
```$ pip install -r requirements.txt ```
7. Execute migrations and migrate models in accordance with Django:
``` $ python3 manage.py makemigrations ``` or in short form you can use makefile ```$ make makemigrations```
```$ python3 manage.py migrate ```  or in short  you can use ``` $ make migrate```
 
8. Optional: Create a super user using the following commands for admin view.
```$ python3  manage.py createsuperuser ``` or you can use short command ```$ make superuser```
9. Run the server. ```$ python3 manage.py  runserver ``` or you can user short caommand ```$ make run```

# How to make a request to the  server/test it?
 - Please import the retispec.postman_collection.json file into Postman (https://www.postman.com/downloads/) after installing Postman. There, you can use the API calls mentioned in the JSON document via its GUI.
 - Alternatively, go to ```$ localhost:8000/swagger/``` and test it via swagger GUI.
###                                          Thank  You!
#                                            September 22,2022
