FROM python:3.6
COPY ./requirements.txt /srv/requirements.txt
COPY ./requirements-unqualified.txt /srv/requirements-unqualified.txt
RUN pip install -r /srv/requirements.txt