
FROM gcc
WORKDIR /usr/src/app
COPY . .
#ENTRYPOINT [ "sh -c" ]

# this prevents the container to run
#CMD apt install -y python3-pip

RUN apt update
RUN apt install -y python3-pip
RUN pip3 install requests
RUN pip3 install psutil
RUN pip3 install flask
# optional
RUN apt install -y curl

#<pre>docker: Error response from daemon: OCI runtime create failed: container_linux.go:380: starting container process caused: exec: &quot;pip3&quot;: executable file not found in $PATH: unknown.</pre>
#CMD ["pip3", "install", "requests"]
