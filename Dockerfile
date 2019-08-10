FROM python:3.6-slim
COPY . /web
WORKDIR /web
RUN pip install -r ./requirements.txt
#RUN adduser -D myuser
#USER myuser
ENTRYPOINT ["python"]
CMD ["app.py"]