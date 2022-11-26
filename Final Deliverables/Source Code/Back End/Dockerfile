FROM python:3.10.4-alpine
RUN pip install --upgrade pip
WORKDIR /ibm-news-app
ADD . /ibm-news-app
RUN pip install -r requirements.txt
ENTRYPOINT [ "python" ]
CMD ["main.py"]