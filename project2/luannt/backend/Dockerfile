# Base Image
FROM python:3.9.16

# Install netcat
RUN apt-get update && \
    apt-get -y install netcat && \
    apt-get clean

WORKDIR /backend

COPY ./backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./backend .

# run server
CMD ["python", "app.py"]

EXPOSE 8000