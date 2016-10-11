FROM selenium/standalone-chrome:2.53.1-americium

USER root

COPY . /telehangbot

RUN apt-get update && apt-get install -y python python-pip 
RUN pip install telepot
RUN pip install selenium

RUN chmod +x /telehangbot/entry_point.sh

CMD bash /telehangbot/entry_point.sh

#ENTRYPOINT python /telehangbot/run.py