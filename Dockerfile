#FROM selenium/standalone-chrome:2.53.1-americium
FROM selenium/standalone-chrome-debug:2.53.1-americium

USER root

RUN apt-get update && apt-get install -y python python-pip 
RUN pip install telepot
RUN pip install selenium

COPY . /telehangbot
RUN chmod +x /telehangbot/entry_point.sh

CMD bash /telehangbot/entry_point.sh

#ENTRYPOINT python /telehangbot/run.py