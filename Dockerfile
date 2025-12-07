# DIQQAT: 'slim' versiya emas, to'liq versiya ishlatamiz (build xatosini oldini olish uchun)
FROM python:3.9

# Kerakli tizim paketlari
RUN apt-get update && \
    apt-get install -y poppler-utils git && \
    rm -rf /var/lib/apt/lists/*

# Pipni yangilash
RUN pip install --upgrade pip

# Kutubxonalarni o'rnatish
RUN pip install PyMuPDF
RUN pip install flask git+https://github.com/ashafaei/pdf2pptx.git

# Ishchi papka va kod
WORKDIR /app
COPY app.py .

# Port va start
EXPOSE 5000
CMD ["python", "app.py"]
