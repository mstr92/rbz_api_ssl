# API for rbz.io

## Commands:
- Start docker: docker-compose up --build
- Stop docker: docker-compose down

## Used libraries
- Flask with Swagger
- SqlAlchemy
- RabbitMQ
- Celery

## User-Interfaces and User/Passwords:
- Swagger UI : https://localhost:5000/api/
- RabbitMQ: http://localhost:15672/
    - User: guest
    - Password: guest
- Mysql:
    - User: root
    - Password: root

## Steps to insert a new category:
1. Add a py-file like endpoints/movies.py for the new category. In this file create a new namespace.
2. Add the new namespace to the api in app.py - initialize_app(flask_app)
3. Create a new Model in the file helpers/serializers.py which you can use in the file created in Step 1.
4. Create a new CeleryTaskClass in tasks/tasks.py to make a request to the server. There you should define a new queue.
    - e.g. queue = "games"
5. In the file docker-compose.yml add the new queue to the celery command.
    - e.g. celery -A tasks.tasks worker -Q movies, games -B -l INFO

## Schematic API-flow
![Api-Flow](https://github.com/mstr92/rbz_api/blob/master/api_flow.JPG)