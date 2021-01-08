# Dockerized Angular Application

This application is a simple example of how to use Docker + Angular + Ansible to produce a simple user interface to interact with Kinesis Data Streams. This simple application uses Docker to containerize an Angular app and uses Ansible to load and configure the build/distribution of the Angular application.

1. Build Docker Image
To build the Docker image use the following: `docker image build -t ubuntu-angular .`

2. Run the docker container
Run the docker contianer: `docker run -d -p 80:80 ubuntu-angular`

3. Run app locally
To run the Angular application locally, navigate inside the site directory and use: `ng serve`

4. Docker Installs
Docker installs the ubuntu container and things like apache, ansible, and nodejs.

5. Ansible Configurations
Ansible removes the node_modules, runs npm install, packages the Angular app, and copies the distribution site to the /var/www/html directory.

6. Apache Serves App
Apache serves the application on port 80.
