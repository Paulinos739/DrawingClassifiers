FROM python:3.9-slim-buster
RUN pip3 install Flask waitress tensorflow scipy pandas numpy pillow

WORKDIR /app
COPY src/ .
COPY TrainedModels ./TrainedModels
CMD [ "python3", "server.py"]
