FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/* 

WORKDIR /app

COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -U pip \
 && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["sh", "-c", "streamlit run streamlit_app.py --server.address=0.0.0.0 --server.port=${PORT:-8501} --server.headless=true"]