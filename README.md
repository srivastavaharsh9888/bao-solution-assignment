# bao-solution-assignment
<img width="1710" alt="Screenshot 2023-11-19 at 8 31 18 AM" src="https://github.com/srivastavaharsh9888/bao-solution-assignment/assets/22855779/90ecafc3-55ee-4154-b349-9762fe4cc9c5">



To run the assignment ensure to have redis running locally, celery worker and celery-django-beat successfully installed on your system.

to run celery-beat-:
<br>
celery -A baomovie beat --scheduler django_celery_beat.schedulers:DatabaseScheduler

to run celery worker-:
<br>
celery -A baomovie  worker --loglevel=info 

to run server-:
<br>
python3 manage.py runserver
