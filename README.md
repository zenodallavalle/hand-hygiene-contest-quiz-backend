# Hand-Hygiene-Contest-Quiz-Backend

## Introduction

This repository contains the code for the backend of the Hand Hygiene Contest Quiz. The backend is written in python and uses the django and djangorestframeworks for the REST API.

Since registration is not required for the quiz, the backend stores only the quiz results and user data for statistics.

The frontend is available on GitHub aswell at [https://github.com/zenodallavalle/hand-hygiene-contest-quiz-frontend](this link).

## Setup

The following steps are required to run the frontend locally (python3 required):

1. Clone the repository
2. Create a virtual environment: `python3 -m venv env`
3. Activate the virtual environment: (MacOS or Linux: `source env/bin/activate`) (Windows: `env\Scripts\activate.bat`)
4. Install dependencies: `pip install -r requirements.txt`
5. Edit .env file in the root directory
6. Edit the settings in `hand_hygiene_contest_backend/settings.py` if necessary
7. Apply migrations: `python manage.py migrate`
8. Run the server: `python manage.py runserver`
