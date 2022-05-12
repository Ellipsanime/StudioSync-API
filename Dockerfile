FROM python:3.10
ENV MODULE_NAME app.main:app
ENV HOST 0.0.0.0
ENV PORT 8090
ENV WORKERS 1
ENV WORKER_CLASS uvicorn.workers.UvicornWorker

WORKDIR /code
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y sqlite3 libsqlite3-dev
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY app /code/app
RUN echo type python

CMD ["gunicorn", "${MODULE_NAME}", "-w ${WORKERS}", "-k ${WORKER_CLASS}", "-b ${HOST}:${PORT}"]