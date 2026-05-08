# base image
FROM python:3.10-slim

# work directory
WORKDIR /app

# copy files
COPY . .

# install dependencies
RUN pip install fastapi uvicorn scikit-learn pandas joblib mlflow python-multipart

# expose port
EXPOSE 8000

# run api
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]