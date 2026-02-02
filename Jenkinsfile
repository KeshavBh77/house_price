pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "house-price-api"
        DOCKER_CONTAINER = "house-price-container"
    }

    stages {

        stage('Checkout Code') {
            steps {
                echo "Checking out code from Git"
                checkout scm
            }
        }

        stage('Set Up Python Environment') {
            steps {
                echo "Setting up Python virtual environment"
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip setuptools wheel
                pip install -r requirements.txt
                '''
            }
        }

        stage('Train Model') {
            steps {
                echo "Training ML model"
                sh '''
                . venv/bin/activate
                python train.py
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo "Running tests"
                sh '''
                . venv/bin/activate
                pytest tests/ --maxfail=1 --disable-warnings -q
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image"
                sh "docker build -t ${DOCKER_IMAGE} ."
            }
        }

        stage('Push Docker Image to DockerHub') {
            when {
                expression { return false } // disable for now (enable later)
            }
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKERHUB_USER',
                        passwordVariable: 'DOCKERHUB_PASS'
                    )
                ]) {
                    sh '''
                    echo "$DOCKERHUB_PASS" | docker login -u "$DOCKERHUB_USER" --password-stdin
                    docker tag ${DOCKER_IMAGE} $DOCKERHUB_USER/${DOCKER_IMAGE}:latest
                    docker push $DOCKERHUB_USER/${DOCKER_IMAGE}:latest
                    '''
                }
            }
        }

        stage('Deploy Container') {
            steps {
                echo "Deploying container"
                sh '''
                docker rm -f house-price-container || true
                docker run -d -p 80:5001 --name house-price-container house-price-api
                '''
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully 🎉"
        }
        failure {
            echo "Pipeline failed ❌ — check logs"
        }
    }
}