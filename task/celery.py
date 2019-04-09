from celery import Celery


app = Celery('task', include=['task.spider'])
app.config_from_object('task.celery_config')


if __name__ == '__main__':
    app.start()

# set FORKED_BY_MULTIPROCESSING = 1 or powershell: $env:FORKED_BY_MULTIPROCESSING = 1

# start worker
# celery -A task worker --loglevel=info

# start beat
# celery -A task beat --loglevel=info

# on linux it can start worker and the beat at the same time
# celery -A task beat --loglevel=info -B
