# Docker container:
`docker build -t kategorije-dogodkov .` 
`docker run -d -p 56734:80 --name=kategorije-dogodkov kategorije-dogodkov`

# Pushanje na heroku:
`heroku container:push web --app kategorije-dogodkov`
`heroku container:release web --app kategorije-dogodkov`


## Razlaga `Dockerfile`:
`FROM tiangolo/uwsgi-nginx:python3.8` za osnovo uporabi že ustvarjen docker container (uwsgi, nginx, python3.8)
`RUN apt-get update` posodobi apt-get
`RUN apt-get -y install nano bash` z apt-get naložimo nano in bash (za upravljanje datotek znotraj containerja)
`WORKDIR /app` nastavi workdir
`COPY . .` kopiramo celotno vsebino trenutne mape v ustvarjnei docker contrainer
`RUN pip install --upgrade pip` posodobimo pip
`RUN pip install -r requirements.txt` z pip inštalimarmo vse pakete znotraj requirements.txt datoteke
`COPY ./nltk_data /usr/share/nltk_data` vsebine za paket nltk (nltk.download() ne deluje)
`CMD ["python", "main.py"]` zaženemo main.py
