FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Train model during image build so model.pkl exists
RUN python train.py

EXPOSE 5001

CMD ["python", "app.py"]
