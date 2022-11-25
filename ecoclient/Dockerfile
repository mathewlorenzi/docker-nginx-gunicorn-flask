#FROM python:alpine
#WORKDIR /usr/src/app
#COPY . .
#RUN pip install requests
## useless
## EXPOSE 5555
##CMD ["python", "manager.py", "--url", "http://web", "--port", "8000", "--ecovisionPath", "./package_ecovision"]
#CMD ["python", "manager.py", "--debug", "--url", "http://web", "--port", "8000", "--ecovisionPath", "./package_ecovision"]
# error: FileNotFoundError: [Errno 2] No such file or directory: './package_ecovision/build/bin/platformecpp'

# FROM alpine
# WORKDIR /usr/src/app
# COPY . .
# RUN apk add --no-cache python3 py3-pip
# RUN pip3 install requests
# # useless
# # EXPOSE 5555
# #CMD ["python", "manager.py", "--url", "http://web", "--port", "8000", "--ecovisionPath", "./package_ecovision"]
# CMD ["python", "manager.py", "--debug", "--url", "http://web", "--port", "8000", "--ecovisionPath", "./package_ecovision"]
#ENTRYPOINT [ "python" ]
#ERROR: for ecoclient  Cannot start service ecoclient: OCI runtime create failed: container_linux.go:380: starting container process caused: exec: "python": executable file not found in $PATH: unknown
#ERROR: Encountered errors while bringing up the project.

FROM gcc
WORKDIR /usr/src/app
COPY . .
CMD apt install -y python3-pip
CMD ["pip3", "install", "requests"]
