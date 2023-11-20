# BAO Solution Assignment

![Screenshot](https://github.com/srivastavaharsh9888/bao-solution-assignment/assets/22855779/90ecafc3-55ee-4154-b349-9762fe4cc9c5)

This project is a Django application that interfaces with the Ghibli API to fetch and display movie information. It uses Celery with Redis for task management and scheduling.

## Getting Started

### Prerequisites

Before running the application, ensure you have the following installed:
- Redis (running locally)
- Celery
- Django Celery Beat

### Running the Application

- **Start Celery Beat**
  ```bash
  celery -A baomovie beat --scheduler django_celery_beat.schedulers:DatabaseScheduler

- **To run celery worker:**
  ```bash
  celery -A baomovie worker --loglevel=info

- To run server use-:
  ```bash
  python3 manage.py runserver

### Improvements:

- Move the secret key to .env file.
- Create API docs using Swagger.
- For saving movie and people data we should be doing it through serializers as in task I am writing custom code.
- We can also implement pagination to get faster and limited response but while including pagination we need to take care of caching like what should be the data structure for storing pagination response and if any new video is added then we need to refresh the cache or mark that as outdated.
- Test cases also need to be added.
