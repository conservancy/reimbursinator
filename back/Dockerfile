# pull python base image
FROM python:3.5

# set up enviroment
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set working directory
WORKDIR /usr/src/app

# install dependencies
RUN pip install --upgrade pip
RUN pip install pipenv
COPY ./Pipfile /usr/src/app/Pipfile
RUN pipenv install --skip-lock --system --dev

# copy project
COPY . /usr/src/app/

# copy ssl files
COPY ./ssl/ /etc/ssl/private/
