# I wrote this Dockerfile to run the Python script inside of my container, but it doesn't work because of our Windows auth at work
FROM python:3.8-slim

ENV DEBIAN_FRONTEND="noninteractive"\
  ACCEPT_EULA="y"

# install system dependencies
# Microsoft SQL Server Prerequisites
RUN apt-get update -y \
 && apt-get install -y gcc curl gnupg build-essential\
 unixodbc unixodbc-dev tdsodbc freetds-common freetds-bin freetds-dev\
 && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
 && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
 && apt-get update \
 && apt-get install -y --no-install-recommends locales apt-transport-https\
 && apt-get -y --no-install-recommends install msodbcsql18 unixodbc-dev

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./SQL_Server_ForLoop.py" ]
