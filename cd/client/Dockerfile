FROM python:3.10
ENV MODULE_NAME app.client.main:app
ENV HOST 0.0.0.0
ENV PORT 8091
ENV WORKERS 1
ENV WORKER_CLASS uvicorn.workers.UvicornWorker
ENV DB_PATH /data/db/database.sqlite

WORKDIR /code
RUN mkdir -p /data/db
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y sqlite3 libsqlite3-dev
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN mkdir /code/.tmp
COPY app /code/app
RUN echo type python


RUN /bin/bash -l -c 'echo "gunicorn $MODULE_NAME -w $WORKERS -k $WORKER_CLASS -b $HOST:$PORT " > /code/.tmp/run.sh'
RUN /bin/bash -l -c 'chmod +x /code/.tmp/run.sh'

ENTRYPOINT /code/.tmp/run.sh