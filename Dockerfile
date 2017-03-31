# FROM selenium/standalone-chrome:3.3.0-americium
FROM selenium/standalone-chrome-debug:3.3.0-americium

USER root

RUN apt-get update && apt-get install -y python3 python3-pip 
RUN pip3 install telepot
RUN pip3 install selenium

COPY . /telehangbot
RUN chmod +x /telehangbot/entry_point.sh

CMD bash /telehangbot/entry_point.sh