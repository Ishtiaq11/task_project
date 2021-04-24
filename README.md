# task_project
Task project

# Project Requirements (If run with docker)

1. Docker & Docker-compose
2. Python 3.7
3. Git

# Project Setup
1. Firstly clone the project

2. Goto the project root directory and copy the environment file following the command
    `cp .env .env`
    - update env variable based on docker network host
3. Run the docker following the command
    `docker-compose build`
    then
    `docker-composer up`
4. After the completed check the docker container list
    `docker ps`
5.  Migrate db Using docker container 
        `docker-compose run app /usr/local/bin/python manage.py migrate`
5. Run the app using docker container
        `docker-compose run app /usr/local/bin/python manage.py runserver`
6. Finally run the project with the following url

    `http://0.0.0.0:8000/`

# Project setup (With virtual environment)

1. Firstly clone the project

2. Goto the project root directory and copy the environment file following the command

    `cp .env .env`

	1. Update the postgres database name, host, username, password and schema name or public schema
3. Install the python dependencies following the command

	`pip install -r requirements.txt`

4. Migrate the database

    `python manage.py migrate`
5. Added users from management command

	`python manage.py add_user`

6. Finally run the local server

	`python manage.py runserver`

7. Install rabbitmq server locally
    - For ubuntu user
    `sudo apt-get install rabbitmq-server`


8. Run this command in Terminal 
   `celery -A task_project worker --loglevel=info`


# Run Unit test case
 - python manage.py test survey.tests