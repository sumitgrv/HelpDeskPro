FROM python:3.11-slim

WORKDIR /app
# UI only needs streamlit, requests, and python-dotenv (not the full backend dependencies)
COPY requirements-ui.txt .
RUN pip install --no-cache-dir -r requirements-ui.txt

COPY ui ./ui
COPY .env.example ./.env

EXPOSE 8501
CMD ["streamlit", "run", "ui/streamlit_app.py", "--server.address=0.0.0.0", "--server.port=8501"]
