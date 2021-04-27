FROM tiangolo/uwsgi-nginx:python3.8
RUN apt-get update
RUN apt-get -y install nano bash
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
COPY ./nltk_data /usr/share/nltk_data
CMD ["python", "main.py"]