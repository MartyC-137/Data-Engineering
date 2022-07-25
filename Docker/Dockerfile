# I wrote this Dockerfile to run the Python script inside of my container, but it doesn't work because of our Windows auth at work
FROM python:3.8-slim

# install system dependencies
RUN apt update 
RUN apt-get update -y && apt-get install -y gcc curl gnupg build-essential
RUN apt-get update -y && apt-get install -y unixodbc unixodbc-dev tdsodbc freetds-common freetds-bin freetds-dev

# Microsoft SQL Server Prerequisites
RUN apt-get update && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - 
RUN curl https://packages.microsoft.com/config/debian/9/prod.list > /etc/apt/sources.list.d/mssql-release.list 
RUN apt-get install -y --no-install-recommends locales apt-transport-https 
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && locale-gen
ENV ACCEPT_EULA=y DEBIAN_FRONTEND=noninteractive 
RUN apt-get update && apt-get -y --no-install-recommends install msodbcsql17
# RUN apt-get -qq update && apt-get -yqq install krb5-user libpam-krb5 && apt-get -yqq clean

# RUN apt-get update && ACCEPT_EULA=Y apt-get -y install mssql-tools msodbcsql17
# RUN apk add --no-cache gcc libc-dev unixodbc-dev

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./SQL_Server_ForLoop.py" ]