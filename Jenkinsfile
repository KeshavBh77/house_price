pipeline {
    agent any

    environment {
        // Docker image and container names
        DOCKER_IMAGE = "house-price-api"
        DOCKER_CONTAINER = "house-price-container"

        // Single DockerHub credential (username + password)
        DOCKERHUB_CRED = credentials('dockerhub-username')

        // Ensure Jenkins can find docker
        PATH = "/usr/local/bin:${env.PATH}"
    }

    stages {

        // -------------------------
        stage('Checkout Code') {
            steps {
                echo "Checking out code from Git"
                checkout scm
            }
        }

        // -------------------------
        stage('Set Up Python Environment') {
            steps {
                echo "Creating Python virtual environment and installing dependencies"
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip setuptools wheel
                pip install -r requirements.txt
                '''
            }
        }

        // -------------------------
        stage('Train Model') {
            steps {
                echo "Training the ML model"
                sh '''
                . venv/bin/activate
                python train.py
                '''
            }
        }

        // -------------------------
        stage('Run Tests') {
            steps {
                echo "Running unit tests"
                sh '''
                . venv/bin/activate
                pytest tests/ --maxfail=1 --disable-warnings -q
                '''
            }
        }

        // -------------------------
        stage('Build Docker Image') {
            steps {
                echo "Building Docker image: ${DOCKER_IMAGE}"
                sh "docker build -t ${DOCKER_IMAGE} ."
            }
        }

        // -------------------------
        stage('Optional: Push Docker Image to DockerHub') {
            when {
                expression { return env.DOCKERHUB_CRED != null }
            }
            steps {
                echo "Pushing Docker image to DockerHub"
                sh '''
                echo ${DOCKERHUB_CRED_PSW} | docker login -u ${DOCKERHUB_CRED_USR} --password-stdin
                docker tag ${DOCKER_IMAGE} ${DOCKERHUB_CRED_USR}/${DOCKER_IMAGE}:latest
                docker push ${DOCKERHUB_CRED_USR}/${DOCKER_IMAGE}:latest
                '''
            }
        }

        // -------------------------
        stage('Deploy Container') {
            steps {
                echo "Stopping old container and running new one"
                sh """
                docker rm -f ${DOCKER_CONTAINER} || true
                docker run -d -p 80:5001 --name ${DOCKER_CONTAINER} ${DOCKER_IMAGE}
                """
            }
        }

    }

    post {
        always {
            node {
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