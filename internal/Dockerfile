FROM python:3.10-bullseye
WORKDIR /app

COPY requirements.txt .
RUN pip install --progress-bar off --upgrade pip
RUN pip install --progress-bar off -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh
#CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
