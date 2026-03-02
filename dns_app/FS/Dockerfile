FROM python:3.11-slim


WORKDIR /app

COPY fs.py .

RUN pip install Flask
RUN pip install requests

EXPOSE 9090

CMD ["python", "fs.py"]
