FROM python:3.8

WORKDIR /flask-LLM
ADD . /flask-LLM
RUN pip install -r requirements.txt
CMD [ "python" , "/flask-LLM/app.py" ]

RUN chown -R 42420:42420 /flask-LLM
ENV HOME=/flask-LLM
