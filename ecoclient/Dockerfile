FROM python:alpine

WORKDIR /usr/src/app

COPY . .

RUN pip install requests

# useless
# EXPOSE 5555

CMD ["python", "manager.py", "--url", "http://127.0.0.1", "--port", "8000", "--ecovisionPath", "./package_ecovision"]
