FROM python:3.9-slim

# Kerakli tizim kutubxonalari
RUN apt-get update && \
    apt-get install -y poppler-utils git && \
    rm -rf /var/lib/apt/lists/*

# Python kutubxonalarini o'rnatish
RUN pip install flask git+https://github.com/ashafaei/pdf2pptx.git

WORKDIR /app
COPY app.py .

EXPOSE 5000
CMD ["python", "app.py"]
