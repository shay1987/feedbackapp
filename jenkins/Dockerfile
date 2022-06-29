FROM jenkins/jenkins:lts

USER root

# prerequisites for docker
RUN apt-get update \
    && apt-get install -y \
        curl \
        unzip

# docker repos
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add - \
    && echo "deb [arch=amd64] https://download.docker.com/linux/ubuntu xenial stable" >> /etc/apt/sources.list.d/additional-repositories.list \
    && echo "deb http://ftp-stud.hs-esslingen.de/ubuntu xenial main restricted universe multiverse" >> /etc/apt/sources.list.d/official-package-repositories.list \
    && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 437D05B5 \
    && apt-get update

# docker
RUN apt-get install -y docker-ce

#replace docker group
# RUN groupadd docker

# give jenkins docker rights
RUN gpasswd -a jenkins docker

USER jenkins

