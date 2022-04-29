# syntax=docker/dockerfile:1

FROM python:3.9


WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=3000"]

CMD ["gunicorn","--bind","0.0.0.0:3000","--workers=2","app:app"]
# gunicorn --bind localhost:3000 --workers=2 app:app