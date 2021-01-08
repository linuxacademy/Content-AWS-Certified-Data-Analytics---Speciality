FROM ubuntu:14.04
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