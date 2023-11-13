FROM ubuntu:latest
COPY . .
RUN apt-get -y update
RUN apt install -y python3
RUN apt install -y ffmpeg
RUN apt install -y python3-pip
RUN pip install -r requirements.txt
CMD python3 play.py "8020"