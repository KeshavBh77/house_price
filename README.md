# House Price Prediction API (ML + DevOps)

End-to-end ML project that predicts house prices using a scikit-learn regression model served via a Flask REST API with a simple HTML frontend. The project is fully containerized using Docker, automated with a Jenkins CI/CD pipeline (build, test, Docker image creation, push to DockerHub), and deployed on AWS EC2 for real-world production simulation.

## Tech Stack
Python, Flask, scikit-learn, NumPy, HTML, JavaScript, Docker, Jenkins, AWS EC2

## Run Locally
git clone https://github.com/your-username/house_price.git  
cd house_price  
python3 -m venv venv  
source venv/bin/activate  
pip install -r requirements.txt  
python train.py  
python app.py  
Open: http://localhost:5001

## Docker
docker build -t house-price-api .  
docker run -d -p 5001:5001 house-price-api  

## AWS EC2 Deploy
sudo apt update && sudo apt install docker.io -y  
docker pull your-dockerhub-username/house-price-api:latest  
docker run -d -p 5001:5001 your-dockerhub-username/house-price-api:latest  
Open Security Group port: 5001 (TCP)  
Access: http://<EC2_PUBLIC_IP>:5001

## Jenkins Pipeline
Stages: Git checkout → install deps → test (pytest) → build Docker image → push to DockerHub → deploy to EC2

## API
GET / → health check + UI  
POST /predict → {"bedrooms":3,"bathrooms":2,"area":1500} → {"price":123456.0}

## Result
Fully automated ML deployment pipeline demonstrating CI/CD, containerization, and cloud deployment using AWS EC2.
