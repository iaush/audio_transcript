Audio transcriber Application

Instructions to run application:

    Running via docker:
        - requires docker and docker compose to be installed
        - run "docker-compose up --build" command 
        - frontend will be available at http://localhost:8080
        - backend will be available at http://localhost:8000 or http://localhost:8000/docs for swagger ui

    Running locally via python and node:
        - requires python(pipenv) for backend and nodejs for frontend
        Frontend:
            - run "cd frontendTS/app"
            - run "npm ci"
            - run "npm start"
        Backend:
            - run "cd backend"
            - run "pipenv install"
            - run "pipenv run uvicorn src.main:app"

Instructions for unit testing:

    Frontend:
    - run "cd frontendTS/app"
    - run "npm test"
    
    Backend:
    - requires pytest to be installed 
    - run "cd backend"
    - run "pytest"



