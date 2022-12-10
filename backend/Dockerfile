FROM python:alpine

WORKDIR /usr/src/app

COPY . .

# musl dev + linux heqders and gcc only for python build wheel for psutil ! for the cpu ram info ... do i keep that ?
RUN apk update
RUN apk add musl-dev
RUN apk add linux-headers
RUN apk add gcc

RUN pip install --no-cache-dir -r requirements.txt
#RUN pip install -r requirements.txt
# RUN pip install gunicorn

# CMD ["FLASK_APP=./backend.py", "flask", "run", "-h", "0.0.0.0", "-p", "5555"]
CMD ["python", "backend.py"]
