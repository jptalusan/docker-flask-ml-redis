#FROM resin/raspberrypi3-python:3.6-slim
FROM linusmotu/rpi-jupyter:datascience1.3

WORKDIR /root

#RUN apt-get update
RUN pip3 install --upgrade pip
RUN pip3 install setuptools

# for flask web server
EXPOSE 8081

# set working directory
ADD . /app
WORKDIR /app

# install required libraries
RUN pip3 install -r requirements.txt

# This is the runtime command for the container
RUN echo $(ls -1 /app)
#CMD ["python", "-u", "app.py"]
#CMD python -u app.py
CMD python3 -u app.py


