pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "house-price-api"
        DOCKER_CONTAINER = "house-price-container"
        DOCKERHUB_USER = credentials('dockerhub-username')
        DOCKERHUB_PASS = credentials('dockerhub-password')
        PATH = "/usr/local/bin:$PATH" // Ensures Docker is found
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
                source venv/bin/activate
                pip install --upgrade pip setuptools wheel
                pip install -r requirements.txt
                '''
            }
        }

        stage('Train Model') {
            steps {
                echo "Training ML model"
                sh '''
                source venv/bin/activate
                python train.py
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo "Running unit tests"
                sh '''
                source venv/bin/activate
                pytest tests/ --maxfail=1 --disable-warnings -q
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image: ${DOCKER_IMAGE}"
                sh 'docker build -t ${DOCKER_IMAGE} .'
            }
        }

        stage('Optional: Push Docker Image to DockerHub') {
            when {
                expression { return env.DOCKERHUB_USER != null }
            }
            steps {
                echo "Pushing Docker image to DockerHub"
                sh '''
                echo $DOCKERHUB_PASS | docker login -u $DOCKERHUB_USER --password-stdin
                docker tag ${DOCKER_IMAGE} $DOCKERHUB_USER/${DOCKER_IMAGE}:latest
                docker push $DOCKERHUB_USER/${DOCKER_IMAGE}:latest
                '''
            }
        }

        stage('Deploy Container') {
            steps {
                echo "Stopping old container and running new one"
                sh '''
                docker rm -f ${DOCKER_CONTAINER} || true
                docker run -d -p 80:5001 --name ${DOCKER_CONTAINER} ${DOCKER_IMAGE}
                '''
            }
        }

    }

    post {
        always {
            node { // Fix MissingContextVariableException
                echo "Cleaning up temporary files"
                sh 'rm -rf venv'
            }
        }
        success {
            echo "Pipeline completed successfully!"
        }
        failure {
            echo "Pipeline failed. Check Jenkins logs."
        }
    }
}