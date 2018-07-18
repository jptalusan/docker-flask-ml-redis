#FROM resin/raspberrypi3-python:3.6-slim
FROM linusmotu/rpi-jupyter:datascience1.3

# for flask web server
EXPOSE 8081

WORKDIR /root

# set working directory
ADD . /app
WORKDIR /app

RUN pip3 install --upgrade pip && \
    pip3 install setuptools && \
    pip3 install -r requirements.txt && \
    echo $(ls -1 /app)

CMD python3 -u app.py


