FROM resin/raspberry-pi-python:3.6
ADD . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
RUN bash -c 'cat test.txt'
CMD ["python3", "-u", "app.py"]
