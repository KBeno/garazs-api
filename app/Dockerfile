FROM python:3.7-slim-stretch
# FROM arm32v7/python:3.7-slim-stretch

WORKDIR /garazs

RUN mkdir ./config

# Creating and activating virtualenv
ENV VIRTUAL_ENV=/garazs/garenv

RUN python3 -m venv $VIRTUAL_ENV

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependecies
COPY requirements.txt /garazs/

RUN pip install -r requirements.txt

# Copy app files
COPY garazs.py user.py status.json /garazs/

# Expose port and run the app
EXPOSE 48165

CMD gunicorn -b :48165 -w 1 garazs:app