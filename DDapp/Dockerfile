FROM django

ADD . /staticsite

WORKDIR /staticsite

RUN pip3 install -r requirements.txt

CMD [ "python3", "./manage.py runserver"]