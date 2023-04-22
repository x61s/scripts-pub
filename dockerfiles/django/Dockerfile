FROM python:3.9.1
ADD requirements.txt .
RUN pip install -r requirements.txt
ADD ./project_name /project_name
WORKDIR /project_name

RUN mkdir -p ./static
RUN mkdir -p ./db

RUN python manage.py migrate

ENV DJANGO_SUPERUSER_USERNAME=admin
ENV DJANGO_SUPERUSER_PASSWORD=password
ENV DJANGO_SUPERUSER_EMAIL=admin@email.org
RUN python manage.py createsuperuser --noinput

RUN python manage.py makemigrations
RUN python manage.py migrate

EXPOSE 8000
#ENTRYPOINT ["python","manage.py","runserver","0.0.0.0:8000"]
ENTRYPOINT ["./gunicorn.sh"]



# $ podman build -f ./Dockerfile -t localhost/${projectname} .
# $ podman run --rm -d -p 8000:8000 localhost/${projectname}
