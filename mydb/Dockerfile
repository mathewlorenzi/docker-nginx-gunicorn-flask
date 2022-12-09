FROM python:alpine

WORKDIR /usr/src/app

COPY . .

RUN pip install flask

EXPOSE 5001

# CMD ["FLASK_APP=./mydb.py", "flask", "run", "-h", "0.0.0.0", "-p", "5001"]
CMD ["python", "mydb.py"]
