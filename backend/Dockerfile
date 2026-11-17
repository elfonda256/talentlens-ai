FROM python:3.12-slim
# Tesseract reads scanned CVs (English + Indonesian).
RUN apt-get update \
    && apt-get install -y --no-install-recommends tesseract-ocr tesseract-ocr-ind \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /srv
COPY requirements.txt requirements-e5.txt ./
RUN pip install --no-cache-dir -r requirements.txt
# Build with INSTALL_E5=true to include the multilingual-e5-small stack. The CPU-only PyTorch
# build is installed first, so pip does not pull several GB of GPU libraries a server never uses.
ARG INSTALL_E5=false
ARG E5_MODEL_NAME=intfloat/multilingual-e5-small
RUN if [ "$INSTALL_E5" = "true" ]; then \
        pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch \
        && pip install --no-cache-dir -r requirements-e5.txt; \
    fi
COPY app ./app
COPY data ./data
RUN useradd --create-home appuser && mkdir storage && chown appuser storage
USER appuser
# Bake the model into the image so a fresh container does not download it on the first screening.
RUN if [ "$INSTALL_E5" = "true" ]; then \
        python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('$E5_MODEL_NAME')"; \
    fi
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
