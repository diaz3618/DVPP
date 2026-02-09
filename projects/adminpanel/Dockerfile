FROM python:3.11-slim
WORKDIR /app
RUN pip install flask==2.3.0
COPY app.py .
EXPOSE 5007
CMD ["python", "app.py"]
