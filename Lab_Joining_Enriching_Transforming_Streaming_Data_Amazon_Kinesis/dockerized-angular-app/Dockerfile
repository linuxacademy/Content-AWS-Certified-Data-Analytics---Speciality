FROM ubuntu:20.04
RUN apt-get update -y
RUN apt-get install software-properties-common -y --fix-missing
RUN apt-add-repository ppa:ansible/ansible
RUN apt-get update -y
RUN apt-get install ansible -y
RUN apt-get install apache2 -y
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf
RUN apt-get install curl -y
RUN apt-get install rpm -y
RUN apt-get install gcc g++ make -y
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash -
RUN apt-get install nodejs

RUN mkdir -p /home/ansible/playbooks
RUN mkdir -p /tmp/site

COPY ./ansible.cfg ./hosts /home/ansible/
COPY ./playbooks /home/ansible/playbooks
COPY ./site /tmp/site
WORKDIR /home/ansible
RUN ansible-playbook /home/ansible/playbooks/setup-angular-app.yml

EXPOSE 80
CMD ["apache2ctl", "-D", "FOREGROUND"]

## Below is for development purposes only
# FROM ubuntu:20.04
# RUN apt-get update
# RUN apt-get install curl gcc g++ make git -y
# EXPOSE 4200

# RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
# RUN apt-get install nodejs -y
# RUN npm install -g npm
# RUN npm install -g @angular/cli

# WORKDIR /home/kinesis-live-angular-app

# docker image build -t kinesis-live-image .
# docker run -p 4200:4200 -v /Users/brocktubre/Desktop/Projects/Content-AWS-Certified-Data-Analytics---Speciality/Lab_Joining_Enriching_Transforming_Streaming_Data_Amazon_Kinesis/dockerized-angular-app/:/home/kinesis-live-angular-app/site -it kinesis-live-image
