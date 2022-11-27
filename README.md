# ECO
https://stackoverflow.com/questions/37960226/invalid-type-error-in-docker-compose
https://stackoverflow.com/questions/55862431/how-to-communicate-between-two-containers-using-docker

****** have an ecovision package ******
cd /home/ecorvee/Projects/EcoVision
=== make sure the home dir is set to /usr/src/app 
vim /home/ecorvee/Projects/EcoVision/ecplatform2/configure/configure.txt
docker-compose build
docker run -t -d -v $PWD/shared_folder:/usr/src/app/shared_folder --name ecovision ecovision_ecovision
docker exec -it ecovision bash
./compile.sh
./create_package.sh
exit
=== go back to ecoclient and get the compiled new package === 
cd /home/ecorvee/Projects/WEBAPP/docker-nginx-gunicorn-flask
rm -rf ecoclient/package_ecovision
cp -r /home/ecorvee/Projects/EcoVision/shared_folder/package_ecovision ./ecoclient

****** [LOCAL or VM] build only the web and ecoclient docker containers ****** unless all ois find and just go up
local: cd /home/ecorvee/Projects/WEBAPP/docker-nginx-gunicorn-flask
vm: git clone
docker-compose build
docker-compose up

## 1) Steps to make it work

original read me in next section.

https://certbot.eff.org/instructions?ws=nginx&os=debianbuster

  563  sudo apt install snapd
  564  sudo snap install core
  570  sudo snap install core; sudo snap refresh core
  571  sudo apt-get remove certbot
  572  sudo snap install --classic certbot
  573  sudo ln -s /snap/bin/certbot /usr/bin/certbot
  574  sudo certbot --nginx
  questions qsked: email, and it proposes to create ca for www.ecovision.com -> yes
  OK: https://www.ecovision.ovh/
  when i check /etc/nginx/sites-enabled/ecovision:
    server {
        listen              443 ssl;
            server_name         www.ecovision.ovh;	
            root /var/www/ecovision/html;
            index index.html index.htm index.nginx-debian.html;
            server_name ecovision www.ecovision.ovh;
            location / {
                    try_files $uri $uri/ =404;
            }
        ssl_certificate /etc/letsencrypt/live/www.ecovision.ovh/fullchain.pem; # managed by Certbot
        ssl_certificate_key /etc/letsencrypt/live/www.ecovision.ovh/privkey.pem; # managed by Certbot
    }
    server {
        if ($host = www.ecovision.ovh) {
            return 301 https://$host$request_uri;
        } # managed by Certbot
        listen 80;
        listen [::]:80;
        server_name         www.ecovision.ovh;
        server_name ecovision www.ecovision.ovh;
        return 404; # managed by Certbot


lets try this in docker nginx
systemctl stop nginx    => stop the current one (without docker) above
/etc/letsencrypt/live/www.ecovision.ovh/fullchain.pem
/etc/nginx/conf.d/ is currently empty but will be shared volume with the docker nging folder contains our new config (above with the keys)
backup; cp -r docker nginx ngin-BACKUP
sudo cp /etc/letsencrypt/live/www.ecovision.ovh/fullchain.pem nginx/conf.d/
sudo cp /etc/letsencrypt/live/www.ecovision.ovh/privkey.pem nginx/conf.d/
adapt content of the above file into app.conf: this gives:


test
go inside nginx container and see if it ca access to gunicnr container:
docker exec -it a173325fdc8b bash
    curl http://web:8000
        => hello world => OK


WORKING https://www.ecovision.ovh:81/camera

# Docker NGINX Gunicorn Flask

Basic Flask application running on Gunicorn, a WSGI HTTP server, with NGINX as a reverse proxy server.

## Requirements

Docker and docker-compose.

## Build images

This will build images based on Alpine Linux for Python. An image for NGINX will be build when the services are started for the first time.

```bash
$ docker-compose build
```
## Start the services

```bash
$ docker-compose up -d # --force-recreate
```

To (stop and) recreate the containers before starting the services, use `--force-recreate`.

## List containers 

```bash
$ docker-compose ps
```

Notice that NGINX runs in the foreground (daemon off).

## Hello World

When both containers are up and running you can test the application.

```bash
$ curl 127.0.0.1
{"message":"Hello World!"}
```

## Stop the services

```bash
$ docker-compose stop
```
