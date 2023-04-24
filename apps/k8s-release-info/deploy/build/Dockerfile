FROM python:3.9.1
ADD ./app /app
WORKDIR /app
RUN pip install -r requirements.txt

# This variables will be used in ./gunicorn.sh
ENV FLASK_APP=ari
ENV FLASK_ENV=development
EXPOSE 5000
# ENTRYPOINT ["python","-m","flask","run"]
ENTRYPOINT ["./gunicorn.sh"]

