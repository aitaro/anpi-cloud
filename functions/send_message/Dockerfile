FROM python:3.7

RUN pip install --upgrade pip
WORKDIR /send_message
COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN pip install functions-framework
RUN pip install flask



