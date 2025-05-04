FROM python:3.10
WORKDIR /app
COPY requerimientos.txt .
RUN pip install -r requerimientos.txt
COPY . .
CMD ["python", "app.py"]
